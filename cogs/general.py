

from discord.ext import commands


class General(commands.Cog):
    """Description of what this file does"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create_game", aliases=["create", "creategame"])
    async def create_game(self, ctx):
        content = "Game Created. Just kidding."
        await ctx.send(content)


def setup(bot):
    bot.add_cog(General(bot))
