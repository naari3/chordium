import pychord

from typing import List


class ChordReader(object):
    """
    parse strings and return note names
    """

    def parse(self, user_input: str) -> List[List[str]]:
        chord_names = user_input.split("|")
        return self.chord_names_to_notes(chord_names)

    def chord_names_to_notes(self, chord_names: List[str]) -> List[List[str]]:
        chord_progression = pychord.ChordProgression(chord_names)

        chords = []
        for chord in chord_progression:
            chords.append(self.chord_to_note_names(chord))

        return chords

    def chord_to_note_names(self, chord: pychord.Chord) -> List[str]:
        note_names = []
        for note in chord.components():
            note_names.append(f"{note}4")  # voicing
        return note_names
