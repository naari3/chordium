import discord
from discord.ext import commands

import tempfile


from chordium import ChordPlayer


class Chorder(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.chord_player = ChordPlayer(metronome=False)

    async def cog_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        await ctx.send("err: {}".format(str(error)))

    @commands.command(name="play")
    async def _play(
        self,
        ctx: commands.Context,
        chords: str,
        scale: str = "C",
        instrument: str = "Acoustic Grand Piano",
        bpm: str = "120",
    ):
        """Play specific chords."""

        if scale == "-":
            scale = "C"

        if instrument == "-":
            instrument = "Acoustic Grand Piano"

        if bpm == "-":
            bpm = "120"

        with tempfile.TemporaryFile() as f:
            self.chord_player.make_wav(f, chords, scale, instrument, float(bpm))

            await ctx.send("♪", file=discord.File(f, "chord.wav"))