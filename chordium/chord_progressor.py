import pretty_midi
from typing import List


class ChordProgressor(object):
    def chords_to_notes(
        self,
        chords: List[List[str]],
    ) -> List[pretty_midi.Note]:
        notes = []

        start = 0
        end = 1

        for chord in chords:
            for note_name in chord:
                note_number = pretty_midi.note_name_to_number(note_name)
                note = pretty_midi.Note(
                    velocity=100, pitch=note_number, start=start, end=end
                )
                notes.append(note)
            start += 1
            end += 1

        return notes