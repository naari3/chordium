from .chord_reader import ChordReader
from .chord_progressor import ChordProgressor

from .utils import f64le_to_s32le

from scipy.io import wavfile
from typing import BinaryIO

import pretty_midi
import wave


class ChordPlayer(object):
    """
    main target is handling pretty_midi
    """

    def __init__(self, metronome: bool):
        self.metronome = metronome
        self.chord_reader = ChordReader()
        self.chord_progressor = ChordProgressor()

    def make_wav(
        self, io: BinaryIO, user_input: str, scale: str, instrument: str, bpm: int
    ):
        pcm = self.make_pcm(user_input, scale, instrument, bpm)
        wavfile.write(io, 44100, pcm)

    def make_pcm(self, user_input: str, scale: str, instrument: str, bpm: int):
        pm = pretty_midi.PrettyMIDI(initial_tempo=bpm)
        program = pretty_midi.instrument_name_to_program(instrument)
        instrument = pretty_midi.Instrument(program=program)

        chords = self.chord_reader.parse(user_input, scale)
        notes = self.chord_progressor.chords_to_notes(chords, bpm)

        instrument.notes.extend(notes)

        pm.instruments.append(instrument)

        audio_data = pm.fluidsynth()
        return f64le_to_s32le(audio_data)