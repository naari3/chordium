import pychord
from typing import List, Callable

from .base import Base

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


class Chord(Base):
    def __init__(self, input: str):
        for chord_str, in_c in DEGREE_DICT.items():
            input = input.strip()
            input = input.replace(chord_str, in_c)
        self._chord: pychord.Chord = pychord.Chord(input)

    def _show_progress(self):
        return self._chord.chord

    def to_notes(self, scale: int, voicing: bool) -> List[str]:
        self._chord.transpose(scale)
        if voicing:
            fix_scale: Callable[[str], str] = lambda chord: f"{chord}4"
            notes = list(map(fix_scale, self._chord.components()))
            return notes
        else:
            return self._chord.components_with_pitch(4)
