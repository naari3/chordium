from dotenv import load_dotenv
import os

import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.environ["DISCORD_BOT_TOKEN"]


class Chorder(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="play",
        invoke_without_subcommand=True,
    )
    async def _play(self, ctx: commands.Context):
        """Play specific chords."""

        await ctx.send("play♪")


bot = commands.Bot("$", description="work in progress")
bot.add_cog(Chorder(bot))


@bot.event
async def on_ready():
    print("Logged in as:\n{0.user.name}\n{0.user.id}".format(bot))


bot.run(TOKEN)