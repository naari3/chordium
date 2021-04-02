from discord.ext import commands

from .cogs.chorder import Chorder

import logging


class Chordium(commands.AutoShardedBot):

    logger = logging.Logger

    async def on_ready(self):
        self.add_cog(Chorder(self))
        self.logger.info("Logged in as: {0.user.name} - {0.user.id}".format(self))