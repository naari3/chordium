from dotenv import load_dotenv
import os

import tempfile
import io

import typing

import discord
from discord.ext import commands

import pychord

import pretty_midi
from scipy.io import wavfile

import numpy as np

from typing import List, BinaryIO


class ChordiumException(Exception):
    pass


def f64le_to_s32le(data):
    shifted = data * (2 ** 31 - 1)  # Data ranges from -1.0 to 1.0
    ints = shifted.astype(np.int32)
    return ints


def chord_to_note_names(chord: pychord.Chord) -> List[str]:
    note_names = []
    for note in chord.components():
        note_names.append(f"{note}4")  # voicing
    return note_names


def chords_name_to_notes(chords_name: str) -> List[pretty_midi.Note]:
    chord_names = chords_name.split("|")
    chords = pychord.ChordProgression(chord_names)
    notes = []

    start = 0
    end = 1

    for chord in chords:
        for note_name in chord_to_note_names(chord):
            note_number = pretty_midi.note_name_to_number(note_name)
            note = pretty_midi.Note(
                velocity=100, pitch=note_number, start=start, end=end
            )
            notes.append(note)
        start += 1
        end += 1

    return notes


def write_chord_to_file(chords_name: str, file: BinaryIO):
    pm = pretty_midi.PrettyMIDI()
    violin_program = pretty_midi.instrument_name_to_program("Violin")
    violin = pretty_midi.Instrument(program=violin_program)

    violin.notes.extend(chords_name_to_notes(chords_name))

    pm.instruments.append(violin)

    audio_data = pm.fluidsynth()
    wavfile.write(file, 44100, f64le_to_s32le(audio_data))


load_dotenv()
TOKEN = os.environ["DISCORD_BOT_TOKEN"]


class Chorder(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        await ctx.send("err: {}".format(str(error)))

    @commands.command(name="play")
    async def _play(self, ctx: commands.Context, chords: str):
        """Play specific chords."""

        with tempfile.TemporaryFile() as f:

            write_chord_to_file(chords, f)
            await ctx.send("♪", file=discord.File(f, "chord.wav"))


bot = commands.Bot("$", description="work in progress")
bot.add_cog(Chorder(bot))


@bot.event
async def on_ready():
    print("Logged in as:\n{0.user.name}\n{0.user.id}".format(bot))


bot.run(TOKEN)