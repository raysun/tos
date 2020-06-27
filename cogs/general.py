

from discord.ext import commands
import discord
import consts


class General(commands.Cog):
    """Description of what this file does"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create_game", aliases=["create", "creategame", "cr"])
    async def create_game(self, ctx):
        game_data = self.bot.dbconn.get_active_game_data(ctx.guild.id)
        if (game_data == None or game_data["state"] == "not_running"):
            self.bot.dbconn.create_game((ctx.guild.id, "waiting_on_players", ctx.author.id), ctx.author.name)
            content = "Game created by " + ctx.author.name + ". Waiting for players to join."
        else:
            content = "You may not create a game while another is currently running."
        await ctx.send(content)

    @commands.command(name="cancel_game", aliases=["cancel", "cancelgame", "ca"])
    async def cancel_game(self, ctx):
        game_data = self.bot.dbconn.get_active_game_data(ctx.guild.id)
        if (game_data != None and game_data["state"] == "waiting_on_players"):
            if game_data["host_discord_id"] == ctx.author.id:
                self.bot.dbconn.cancel_game(ctx.guild.id)
                content = "Game cancelled by " + ctx.author.name + "."
            else:
                content = "Only the host of the game is allowed to cancel the game."
        else:
            content = "You may not perform that action right now."
        await ctx.send(content)

    @commands.command(name="join_game", aliases=["join", "joingame", "j"])
    async def join_game(self, ctx):
        game_data = self.bot.dbconn.get_active_game_data(ctx.guild.id)
        if (game_data != None and game_data["state"] == "waiting_on_players"):
            player_data_list = self.bot.dbconn.get_players_in_game(game_data["game_id"])
            if (player_data_list != None):
                found = False
                player_count = 0
                for player_data in player_data_list:
                    player_count += 1
                    if (player_data["discord_player_id"]) == ctx.author.id:
                        content = "You're already in this game, silly!"
                        found = True
                        break
                if (not found):
                    self.bot.dbconn.create_player((game_data["game_id"], ctx.author.name, ctx.author.id, self.bot.dbconn.get_player_count(game_data["game_id"]) + 1, "placeholder_role", "placeholder_alignment", 0, 0))
                    content = "Player " + ctx.author.name + " has joined the game."
                    if (self.bot.dbconn.get_player_count(game_data["game_id"]) == consts.required_player_count):
                        refresh_player_data = self.bot.dbconn.start_game(ctx.guild.id, game_data["game_id"])
                        await ctx.guild.create_category("Mafia Game")
                        for player_data in refresh_player_data:
                            role_name = f"{player_data['game_number']}: {player_data['name']}"
                            user = ctx.guild.get_member(player_data['discord_player_id'])
                            created_role = await ctx.guild.create_role(name=role_name)
                            await user.add_roles(created_role)
                            await created_role.edit(hoist = True)
                        for player_data in refresh_player_data:
                            channel_overwrites = {}
                            for other_player_data in refresh_player_data:
                                if (other_player_data == player_data):
                                    channel_overwrites[discord.utils.get(ctx.guild.roles,name = f"{other_player_data['game_number']}: {other_player_data['name']}")] = discord.PermissionOverwrite(read_messages = True)
                                else:
                                    channel_overwrites[discord.utils.get(ctx.guild.roles,name = f"{other_player_data['game_number']}: {other_player_data['name']}")] = discord.PermissionOverwrite(read_messages = False)
                            await ctx.guild.create_text_channel(name=f"player-{player_data['game_number']}",
                                                                overwrites=channel_overwrites,
                                                                category=discord.utils.get(ctx.guild.categories, name="Mafia Game"))
                        content += "\nRequired player count has been reached, so the game has started."
            else:
                content = "Ruh roh! We've run into an issue. There seems to be nobody in this game... please retry the command."
        else:
            content = "You may not perform that action right now."
        await ctx.send(content)

    @commands.command(name="leave_game", aliases=["leave", "leavegame", "l"])
    async def leave_game(self, ctx):
        game_data = self.bot.dbconn.get_active_game_data(ctx.guild.id)
        if (game_data != None and game_data["state"] == "waiting_on_players"):
            player_data_list = self.bot.dbconn.get_players_in_game(game_data["game_id"])
            if (player_data_list != None):
                found = False
                player_count = 0
                for player_data in player_data_list:
                    player_count += 1
                    if (player_data["discord_player_id"]) == ctx.author.id:
                        found = True
                        break
                if (found):
                    self.bot.dbconn.remove_player(ctx.author.id)
                    if (self.bot.dbconn.get_player_count(game_data["game_id"]) < 1):
                        await self.cancel_game(ctx)
                        content = "Player " + ctx.author.name + " has left the game.\nThere are no more players in this game, and so it has been cancelled."
                    else:
                        if (ctx.author.id == game_data["host_discord_id"]):
                            new_host = self.bot.dbconn.set_new_host(ctx.guild.id)
                            content = "Host " + ctx.author.name + " has left the game. Thus, the new host is now " + new_host["name"] + "."
                        else:
                            content = "Player " + ctx.author.name + " has left the game."
                else:
                    content = "You do not appear to currently be in a game."
            else:
                content = "Ruh roh! We've run into an issue. There seems to be nobody in this game... please retry the command."
        else:
            content = "You may not perform that action right now."
        await ctx.send(content)

    @commands.command(name="set_prefix", aliases=["prefix"])
    async def set_prefix(self, ctx, newPrefix = None):
        if (newPrefix == None or newPrefix == " "):
            content = "The prefix command requires you to enter a character or set of characters after the command."
        else:
            self.bot.dbconn.change_prefix((newPrefix, ctx.guild.id))
            content = "Bot prefix changed to " + newPrefix

        await ctx.send(content)

    @commands.command(name="get_players", aliases=["players", "pl"])
    async def get_players(self, ctx):
        game_data = self.bot.dbconn.get_active_game_data(ctx.guild.id)
        if (game_data != None and game_data["state"] != "not_running"):
            player_data_list = self.bot.dbconn.get_players_in_game(game_data["game_id"])
            player_count = self.bot.dbconn.get_player_count(game_data["game_id"])
            if (player_count > 1):
                content = "There are " + str(player_count) + " players in game:\n"
            else:
                content = "There is " + str(player_count) + " player in game:\n"
            i = 0
            if (player_data_list != None):
                for player_data in player_data_list:
                    if (i != 0):
                        if (i == player_count - 1 and player_count > 2):
                            content += ", and " + player_data["name"] + "."
                        elif ((i == player_count - 1 and player_count == 2)):
                            content += " and " + player_data["name"] + "."
                        else:
                            content += ", " + player_data["name"]
                    else:
                        content += player_data["name"]
                    i += 1
            else:
                content = "Ruh roh! We've run into an issue. There seems to be nobody in this game... please retry the command."
        else:
            content = "You may not perform that action right now."
        await ctx.send(content)

    @commands.command(name="remove_game", aliases=["remove", "removegame"])
    async def remove_game(self, ctx):
        game_data = self.bot.dbconn.get_active_game_data(ctx.guild.id)
        if game_data != None and game_data["state"] != "not_running" and game_data["state"] != "waiting_on_players" and game_data["host_discord_id"] == ctx.author.id:
            content = "Wow! "
            if discord.utils.get(ctx.guild.categories, name = "Mafia Game") != None:
                await discord.utils.get(ctx.guild.categories, name="Mafia Game").delete()
                content += "Category removed. "
            player_data_list = self.bot.dbconn.get_players_in_game(self.bot.dbconn.get_id_from_server(ctx.guild.id))
            for player_data in player_data_list:
                if discord.utils.get(ctx.guild.roles, name = f"{player_data['game_number']}: {player_data['name']}") != None:
                    await discord.utils.get(ctx.guild.roles, name = f"{player_data['game_number']}: {player_data['name']}").delete()
                    content += "Player role removed. "
                if discord.utils.get(ctx.guild.text_channels, name = f"player-{player_data['game_number']}") != None:
                    await discord.utils.get(ctx.guild.text_channels, name = f"player-{player_data['game_number']}").delete()
                    content += "Channel removed. "
            if (game_data["state"] != "not_running"):
                self.bot.dbconn.cancel_game(ctx.guild.id)
                content += "Game cancelled."
        else:
            if game_data == None:
                content = "There is no game currently logged in our database for this server, so this command cannot be run."
            elif game_data["state"] == "not_running" or game_data["state"] == "waiting_on_players":
                content = "This command can only be performed while the game is running. If there are excess roles or channels, something has gone wrong and you may have to manually remove them."
            else:
                content = "Only the host of the game is allowed to remove the game."
        await ctx.send(content)

def setup(bot):
    bot.add_cog(General(bot))
