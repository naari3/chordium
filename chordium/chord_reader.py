import pychord

from typing import List

DEGREE_DICT = dict(
    sorted(
        {
            "I": "C",
            "II": "D",
            "III": "E",
            "IV": "F",
            "V": "G",
            "VI": "A",
            "VII": "B",
        }.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    )
)


class ChordReader(object):
    """
    parse strings and return note names
    """

    def parse(self, user_input: str, scale: str) -> List[List[str]]:
        chord_names = self._parse(user_input)
        return self.chord_names_to_notes(chord_names, self.scale_to_int(scale))

    def scale_to_int(self, scale: str):
        try:
            scale = int(scale, base=10)
        except ValueError:
            scale = pychord.constants.NOTE_VAL_DICT[scale]
        return scale

    def _parse(self, user_input: str) -> List[str]:
        chords = []
        chord_names = user_input.split("|")
        for chord_name in chord_names:
            for degree, in_c in DEGREE_DICT.items():
                chord_name = chord_name.strip()
                chord_name = chord_name.replace(degree, in_c)
            chords.append(chord_name)

        return chords

    def chord_names_to_notes(
        self, chord_names: List[str], scale: int
    ) -> List[List[str]]:
        chord_progression = pychord.ChordProgression(chord_names)
        chord_progression.transpose(scale)

        chords = []
        for chord in chord_progression:
            chords.append(self.chord_to_note_names(chord))

        return chords

    def chord_to_note_names(self, chord: pychord.Chord) -> List[str]:
        note_names = []
        for note in chord.components():
            note_names.append(f"{note}4")  # voicing
        return note_names
