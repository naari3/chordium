import discord
from discord.ext import commands

import tempfile


from chordium import ChordPlayer


class Chorder(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.chord_player = ChordPlayer(
            instrument="Acoustic Grand Piano", bpm=120, metronome=False
        )

    async def cog_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        await ctx.send("err: {}".format(str(error)))

    @commands.command(name="play")
    async def _play(self, ctx: commands.Context, chords: str):
        """Play specific chords."""

        with tempfile.TemporaryFile() as f:

            self.chord_player.make_wav(chords, f)

            await ctx.send("♪", file=discord.File(f, "chord.wav"))