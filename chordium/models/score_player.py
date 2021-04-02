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

    def make_music(self, wav_io: BinaryIO, midi_io: BinaryIO, notes):
        pm = self._make_pm(notes)
        self._make_midi(pm, midi_io)
        pcm = self._make_pcm(pm)
        wavfile.write(wav_io, 44100, pcm)

    def _make_pcm(self, pm: pretty_midi.PrettyMIDI):
        audio_data = pm.fluidsynth()
        return f64le_to_s32le(audio_data)

    def _make_midi(self, pm: pretty_midi.PrettyMIDI, io: BinaryIO):
        pm.write(io)
        io.seek(0)

    def _make_pm(self, notes):
        pm = pretty_midi.PrettyMIDI()
        program = pretty_midi.instrument_name_to_program(self.instrument_name)
        instrument = pretty_midi.Instrument(program=program)

        instrument.notes.extend(notes)

        pm.instruments.append(instrument)

        return pm
