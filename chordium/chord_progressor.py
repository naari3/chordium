import pretty_midi
from typing import List

import random


class ChordProgressor(object):
    def chords_to_notes(
        self, chords: List[List[str]], bpm: float
    ) -> List[pretty_midi.Note]:
        notes = []

        note_length = 2  # It's half note when bpm 60

        bpm_multiplexer = 60 / bpm

        start = 0
        end = note_length * bpm_multiplexer

        for chord in chords:
            for note_name in chord:
                note_number = pretty_midi.note_name_to_number(note_name)
                note = pretty_midi.Note(
                    velocity=100,
                    pitch=note_number,
                    start=start + random.random() * 0.03,
                    end=end,
                )
                notes.append(note)
            start += note_length * bpm_multiplexer
            end += note_length * bpm_multiplexer

        return notes

    def metronome_notes(
        self, chords: List[List[str]], bpm: float
    ) -> List[pretty_midi.Note]:
        notes = []

        note_length = 2  # It's quarter note when bpm 60

        bpm_multiplexer = 60 / bpm

        start = 0
        end = note_length * bpm_multiplexer

        for _ in range(len(chords)):
            for j in range(4):
                note = pretty_midi.Note(
                    velocity=100,
                    pitch=56,
                    start=start + j * bpm_multiplexer,
                    end=end,
                )
                notes.append(note)
            start += note_length * bpm_multiplexer
            end += note_length * bpm_multiplexer

        return notes