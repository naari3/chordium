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

    def __init__(self):
        self.chord_reader = ChordReader()
        self.chord_progressor = ChordProgressor()

    def make_wav(
        self,
        io: BinaryIO,
        user_input: str,
        scale: str,
        instrument: str,
        bpm: int,
        voicing: bool,
        metronome: bool,
    ):
        pcm = self.make_pcm(user_input, scale, instrument, bpm, voicing, metronome)
        wavfile.write(io, 44100, pcm)

    def make_pcm(
        self,
        user_input: str,
        scale: str,
        instrument_name: str,
        bpm: int,
        voicing: bool,
        metronome: bool,
    ):
        pm = pretty_midi.PrettyMIDI(initial_tempo=bpm)
        program = pretty_midi.instrument_name_to_program(instrument_name)
        instrument = pretty_midi.Instrument(program=program)

        chords = self.chord_reader.parse(user_input, scale, voicing)
        notes = self.chord_progressor.chords_to_notes(chords, bpm)

        instrument.notes.extend(notes)

        pm.instruments.append(instrument)

        if metronome:
            metronome_instrument = pretty_midi.Instrument(program=program, is_drum=True)
            metronome_instrument.notes.extend(
                self.chord_progressor.metronome_notes(chords, bpm)
            )

            pm.instruments.append(metronome_instrument)

        audio_data = pm.fluidsynth()
        return f64le_to_s32le(audio_data)