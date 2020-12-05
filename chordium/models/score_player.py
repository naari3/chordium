from chordium.utils import f64le_to_s32le

from scipy.io import wavfile
from typing import BinaryIO

import pretty_midi
import wave

from dataclasses import dataclass


@dataclass
class ScorePlayer:
    """
    main target is handling pretty_midi
    """

    instrument_name: str

    def make_wav(self, io: BinaryIO, notes):
        pcm = self._make_pcm(notes)
        wavfile.write(io, 44100, pcm)

    def _make_pcm(self, notes):
        pm = pretty_midi.PrettyMIDI()
        program = pretty_midi.instrument_name_to_program(self.instrument_name)
        instrument = pretty_midi.Instrument(program=program)

        instrument.notes.extend(notes)

        pm.instruments.append(instrument)

        # if metronome:
        #     metronome_instrument = pretty_midi.Instrument(program=program, is_drum=True)
        #     metronome_instrument.notes.extend(
        #         self.chord_progressor.metronome_notes(chords, bpm)
        #     )

        #     pm.instruments.append(metronome_instrument)

        audio_data = pm.fluidsynth()
        return f64le_to_s32le(audio_data)