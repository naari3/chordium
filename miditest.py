import pretty_midi
from scipy.io import wavfile

import numpy as np


class ChordiumException(Exception):
    pass


class IDontKnowThatChord(ChordiumException):
    pass


def f64le_to_s32le(data):
    shifted = data * (2 ** 31 - 1)  # Data ranges from -1.0 to 1.0
    ints = shifted.astype(np.int32)
    return ints


def chord_name_to_note_name(chord: str):
    if chord == "C":
        return ["C4", "E4", "G4"]
    else:
        raise IDontKnowThatChord(f'idk that chord "{chord}" yet.')


def chord_to_wav(chord: str):
    pm = pretty_midi.PrettyMIDI()
    violin_program = pretty_midi.instrument_name_to_program("Violin")
    violin = pretty_midi.Instrument(program=violin_program)

    for note_name in chord_name_to_note_name(chord):
        note_number = pretty_midi.note_name_to_number(note_name)
        note = pretty_midi.Note(velocity=100, pitch=note_number, start=0, end=0.5)
        violin.notes.append(note)

    pm.instruments.append(violin)

    audio_data = pm.fluidsynth()
    wavfile.write("hoge.wav", 44100, f64le_to_s32le(audio_data))


if __name__ == "__main__":
    chord_to_wav("C")