import discord
from discord.ext import commands

import tempfile


from chordium.models import ScoreParser, ScorePlayer
from chordium.utils import scale_to_int


class Chorder(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        await ctx.send("err: {}".format(str(error)))
        raise error

    @commands.command(name="play")
    async def _play(
        self,
        ctx: commands.Context,
        chords: str,
        scale: str = "C",
        instrument: str = "Acoustic Grand Piano",
        bpm: str = "120",
        metronome: str = "false",
    ):
        """Play specific chords."""

        self.bot.logger.info(f"{ctx.author}: {ctx.message.content}")

        if scale == "-":
            scale = "C"

        if instrument == "-":
            instrument = "Acoustic Grand Piano"

        if bpm == "-":
            bpm = "120"

        if metronome == "-":
            metronome = "false"

        if metronome in ("yes", "y", "true", "t", "1", "enable", "on"):
            metronome = True
        elif metronome in ("no", "n", "false", "f", "0", "disable", "off"):
            metronome = False

        with tempfile.TemporaryFile() as f:
            progression = ScoreParser().parse(chords, float(bpm))
            player = ScorePlayer(instrument)
            notes = progression.to_notes(scale_to_int(scale))
            player.make_wav(f, notes)

            await ctx.send(
                f"*♪* {progression.show_progress()}", file=discord.File(f, "chord.wav")
            )

        self.bot.logger.debug("played")
