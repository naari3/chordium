import pychord
from typing import List, Callable

from .base import Base


class Chord(Base):
    def __init__(self, input: str):
        self._chord: pychord.Chord = pychord.Chord(input)

    def __repr__(self):
        return f"<Chord: {self._show_progress()}>"

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
