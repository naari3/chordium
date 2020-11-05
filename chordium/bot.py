from discord.ext import commands

from .cogs.chorder import Chorder


class Chordium(commands.AutoShardedBot):
    async def on_ready(self):
        self.add_cog(Chorder(self))
        print("Logged in as:\n{0.user.name}\n{0.user.id}".format(self))