from dotenv import load_dotenv
import os

import tempfile
import io

import typing

import discord
from discord.ext import commands

import pretty_midi
from scipy.io import wavfile

import numpy as np

from typing import List, BinaryIO


class ChordiumException(Exception):
    pass


class IDontKnow(ChordiumException):
    pass


def f64le_to_s32le(data):
    shifted = data * (2 ** 31 - 1)  # Data ranges from -1.0 to 1.0
    ints = shifted.astype(np.int32)
    return ints


def chord_name_to_note_names(chord: str):
    if chord == "C":
        return ["C4", "E4", "G4"]
    else:
        raise IDontKnow(f'idk that chord "{chord}" yet.')


def chord_name_to_notes(chord: str) -> List[pretty_midi.Note]:
    notes = []
    for note_name in chord_name_to_note_names(chord):
        note_number = pretty_midi.note_name_to_number(note_name)
        note = pretty_midi.Note(velocity=100, pitch=note_number, start=0, end=0.5)
        notes.append(note)

    return notes


def write_chord_to_file(chord: str, file: BinaryIO):
    pm = pretty_midi.PrettyMIDI()
    violin_program = pretty_midi.instrument_name_to_program("Violin")
    violin = pretty_midi.Instrument(program=violin_program)

    violin.notes.extend(chord_name_to_notes(chord))

    pm.instruments.append(violin)

    audio_data = pm.fluidsynth()
    wavfile.write(file, 44100, f64le_to_s32le(audio_data))


load_dotenv()
TOKEN = os.environ["DISCORD_BOT_TOKEN"]


class Chorder(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="play")
    async def _play(self, ctx: commands.Context, chord: str):
        """Play specific chord."""

        with tempfile.TemporaryFile() as f:

            write_chord_to_file(chord, f)
            await ctx.send("♪", file=discord.File(f, "chord.wav"))


bot = commands.Bot("$", description="work in progress")
bot.add_cog(Chorder(bot))


@bot.event
async def on_ready():
    print("Logged in as:\n{0.user.name}\n{0.user.id}".format(bot))


bot.run(TOKEN)