from chordium.constants import (
    DEGREE_DICT,
    TONE_DICT,
    TONE_FROM_MUSTHE,
    INV_TONE_DICT,
    note_with_oct,
    note,
    signature,
)
import pychord
from typing import List, Callable
import musthe
import pytheory
import re

from .base import Base

note_with_oct_regex = re.compile(note_with_oct)


class Chord(Base):
    def __init__(self, input: str):
        for chord_str, in_c in DEGREE_DICT.items():
            input = input.strip()
            input = input.replace(chord_str, in_c)
        input = input.replace("on", "/")
        self._chord: str = input

    def _show_progress(self):
        return self._chord

    def to_notes(self, scale: int = 0) -> List[str]:
        chord_str = self._chord
        for t, v in TONE_FROM_MUSTHE.items():
            if t in chord_str:
                chord_str = chord_str.replace(t, v)
        splitted = chord_str.split("/")
        if len(splitted) != 1:
            chord, on = splitted
        else:
            chord = splitted[0]
            on = None

        notes = chord_translate(chord, scale)
        print(chord, notes)

        notes = add_juicy(notes)
        if on:
            notes = add_new_root_notes(notes, transpose_without_oct(on, scale))

        return notes


def add_juicy(notes):
    max_notes = 5
    min_notes = 3
    original_note_len = len(notes)

    for i in range(max_notes - original_note_len):
        j = i + original_note_len - min_notes
        notes.append(up_octave(notes[j]))

    return notes


def up_octave(note) -> str:
    return (musthe.Note(note) + musthe.Interval("P8")).scientific_notation()


add = f"((add)?({signature})(11|13|2|4|6|9){{1}})"
omit = f"((omit|no)(11|13|1|3|5|7|9){{1}})"
add_regex = re.compile(add)
omit_regex = re.compile(omit)


def chord_translate(chord_str: str, scale: int, base_oct: int = 3) -> List[str]:
    try:
        chord = pychord.Chord(chord_str)
        addomit = dict()
    except ValueError as e:
        # add omit だけ抜き取りたい
        chord_without_quality = re.sub(f"^{note}", "", chord_str)
        valid_qualities = list(pychord.quality.QUALITY_DICT.keys())
        valid_qualities.remove("")
        valid_qualities.sort(key=len, reverse=True)

        found = False
        addomit_str = ""
        for quality in valid_qualities:
            if chord_without_quality.find(quality) == 0:  # 先頭のコードqualityを削除する
                found = True
                addomit_str = re.sub(f"^{quality}", "", chord_without_quality)
                chord = pychord.Chord(re.sub(f"{addomit_str}$", "", chord_str))
                break
        if not found:
            raise e

        addomit = {
            "adds": [r.groups()[-2:] for r in re.finditer(add_regex, addomit_str)],
            "omits": [r.groups()[-1] for r in re.finditer(omit_regex, addomit_str)],
        }

    if len(addomit) > 0:
        s = musthe.Scale(f"{chord.root}3", "major")
        adds = addomit.get("adds")
        omits = addomit.get("omits")
        for add in adds:
            align = add[0].count("#") - add[0].count("b")

            adder_note_dict = parse_note_str(
                transpose(s[int(add[1]) - 1].scientific_notation(), align)
            )
            chord.quality.append_note(
                adder_note_dict["note"], chord._root, int(adder_note_dict["oct"]) - 3
            )

        for omit in omits:
            for o in range(int(omit) - 2, int(omit) + 1):
                if o in chord.quality.components:
                    chord.quality.components.remove(o)

    chord.transpose(scale)
    notes = chord.components_with_pitch(base_oct)

    return notes


def add_new_root_notes(notes: List[str], on: str, base_oct: int = 3):
    if musthe.Note(notes[0]).number > musthe.Note(f"{on}{base_oct}").number:
        adjust = 0
    else:
        adjust = -1
    notes.insert(0, f"{on}{base_oct + adjust}")
    return notes


def transpose_notes(notes: List[str], scale: int):
    new_notes = []
    for n in notes:
        new_notes.append(transpose(n, scale))
    return new_notes


def transpose(note: str, scale: int):
    notedict = parse_note_str(note)
    note = notedict["note"]
    oct = int(notedict["oct"])
    note_number = TONE_DICT[TONE_FROM_MUSTHE[note]] + scale
    if note_number > 11:
        oct += 1
    elif note_number < 0:
        oct -= 1
    note_number %= 12
    new_note = INV_TONE_DICT[note_number]
    return f"{new_note}{oct}"


def transpose_without_oct(note: str, scale: int):
    note_number = (TONE_DICT[note] + scale) % 12
    new_note = INV_TONE_DICT[note_number]
    return f"{new_note}"


def parse_note_str(note: str):
    return note_with_oct_regex.search(note).groupdict()
