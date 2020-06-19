

from discord.ext import commands


class General(commands.Cog):
    """Description of what this file does"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create_game", aliases=["create", "creategame"])
    async def create_game(self, ctx):
        game_data = self.bot.dbconn.get_active_game_data(ctx.guild.id)
        if (game_data == None or game_data["state"] == "not_running"):
            self.bot.dbconn.create_game((ctx.guild.id, "waiting_on_players", ctx.author.id))
            content = "Game created by " + ctx.author.name + ". Waiting for players to join."
        else:
            content = "You may not create a game while another is currently running."
        await ctx.send(content)

    @commands.command(name="cancel_game", aliases=["cancel", "cancelgame"])
    async def cancel_game(self, ctx):
        game_data = self.bot.dbconn.get_active_game_data(ctx.guild.id)
        if (game_data != None and game_data["state"] == "waiting_on_players"):
            if (game_data["host_discord_id"] == ctx.author.id):
                self.bot.dbconn.cancel_game(ctx.guild.id)
                content = "Game cancelled by " + ctx.author.name + "."
            else:
                content = "Only the host of the game is allowed to cancel the game."
        else:
            content = "You may not perform that action right now."
        await ctx.send(content)

    @commands.command(name="join_game", aliases=["join", "joingame", "enter", "entergame"])
    async def join_game(self, ctx):
        game_data = self.bot.dbconn.get_active_game_data(ctx.guild.id)
        if (game_data != None and game_data["state"] == "waiting_on_players"):
            if (game_data["host_discord_id"] == ctx.author.id):
                self.bot.dbconn.cancel_game(ctx.guild.id)
                content = "Game cancelled by " + ctx.author.name + "."
            else:
                content = "Only the host of the game is allowed to cancel the game."
        else:
            content = "You may not perform that action right now."
        await ctx.send(content)

    @commands.command(name="set_prefix", aliases=["prefix"])
    async def set_prefix(self, ctx, newPrefix = None):
        self.bot.dbconn.change_prefix((newPrefix, ctx.guild.id))
        content = "Bot prefix changed to " + newPrefix

        await ctx.send(content)


def setup(bot):
    bot.add_cog(General(bot))
