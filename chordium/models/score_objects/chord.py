from chordium.constants import (
    DEGREE_DICT,
    TONE_DICT,
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
        splitted = self._chord.split("/")
        if len(splitted) != 1:
            chord, on = splitted
        else:
            chord = splitted[0]
            on = None

        notes = chord_translate(chord, scale)

        # notes = transpose_notes(notes, scale)
        notes = add_juicy(notes)
        if on:
            notes = add_new_root_notes(notes, transpose_without_oct(on, scale))

        print(notes)
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


add = f"((add)?({signature})?(11|13|5|7|9){1})"
omit = f"((omit|no)?({signature})?(11|13|5|7|9){1})"
add_regex = re.compile(add)
omit_regex = re.compile(omit)


def chord_translate(chord_str: str, scale: int, base_oct: int = 3) -> List[str]:
    try:
        chord = pychord.Chord(chord_str)
        addomit = dict()
    except ValueError as e:
        raise e  # まだ完成してないのでそのままraiseさせる
        # add omit だけ抜き取りたい
        chord_without_quality = re.sub(f"^{note}", "", chord_str)
        valid_qualities = pychord.quality.QUALITY_DICT.keys()
        valid_qualities.remove("")
        valid_qualities.sort(key=len, reverse=True)

        found = False
        addomit_str = ""
        for quality in valid_qualities:
            if chord_without_quality.find(quality) == 0:  # 先頭のコードqualityを削除する
                found = True
                addomit_str = chord_without_quality.lstrip(quality)
                chord = pychord.Chord(chord_str.rstrip(addomit_str))
                break
        if not found:
            raise e

        adds = [r.groups()[-2:] for r in re.finditer(add_regex, addomit_str)]
        omits = [r.groups()[-2:] for r in re.finditer(omit_regex, addomit_str)]

        addomit = {adds: adds, omits: omits}

    if len(addomit) > 0:
        # chord.quality.append_note("", "C") こんなかんじでaddすべきものを逐次追加していく
        # scale = musthe.Scale(chord.root, "major")
        pass

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
    note_number = TONE_DICT[note] + scale
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


# REGEX = re.compile(
#     r"([+＋⁺₊﹢])|([‑‑⁻₋﹣−˗ー－-])|([／/＼\\])|([AaＡａ][DdＤｄ]{2})|([OoＯｏ0０][MmＭｍ][IiＩｉ][TtＴｔ]|[NnＮｎ][OoＯｏ0０])|([DdＤｄ][OoＯｏ0０][MmＭｍ](?![IiＩｉ][TtＴｔ])(?:[IiＩｉ](?:[NnＮｎ](?:[AaＡａ](?:[NnＮｎ][TtＴｔ]?)?)?)?)?)|([AaＡａ][UuＵｕ][GgＧｇ](?:[MmＭｍ][EeＥｅ](?:[NnＮｎ](?:[TtＴｔ](?:[EeＥｅ][DdＤｄ]?)?)?)?)?)|([OoＯｏ0０][NnＮｎ])|([DdＤｄ][IiＩｉ][MmＭｍ](?:[IiＩｉ](?:[NnＮｎ](?:[IiＩｉ](?:[SsＳｓ](?:[HhＨｈ](?:[EeＥｅ][DdＤｄ]?)?)?)?)?)?)?|[°ºᵒ˚⁰∘゜ﾟ○◦◯⚪⭕￮⭘OoＯｏ0０])|([HhＨｈ](?:[AaＡａ](?:[LlＬｌ][FfＦｆ]?)?)?[-‑‑⁻₋﹣−˗ー－ 	  -   　]*[DdＤｄ][IiＩｉ][MmＭｍ](?:[IiＩｉ](?:[NnＮｎ](?:[IiＩｉ](?:[SsＳｓ](?:[HhＨｈ](?:[EeＥｅ][DdＤｄ]?)?)?)?)?)?)?|[øØ∅⌀])|([SsＳｓ][UuＵｕ][SsＳｓ](?:[PpＰｐ](?:[EeＥｅ](?:[NnＮｎ](?:[DdＤｄ](?:[EeＥｅ][DdＤｄ]?)?)?)?)?)?)|([MmＭｍ][aａ](?![UuＵｕ][GgＧｇ]|[DdＤｄ]{2})(?:[JjＪｊ](?:[OoＯｏ0０][RrＲｒ]?)?)?|[MＭΔ△∆▵])|([MmＭｍ][IiＩｉ](?:[NnＮｎ](?:[OoＯｏ0０][RrＲｒ]?)?)?|[mｍ])|([（【\(])|([）】\)])|([。．，、・,.])|([RrＲｒ][OoＯｏ0０]{2}[TtＴｔ])|((?:[EeＥｅ][LlＬｌ][EeＥｅ][VvＶｖ][EeＥｅ][NnＮｎ]|[1１]{2})(?:[TtＴｔ][HhＨｈ])?)|((?:[TtＴｔ][HhＨｈ][IiＩｉ][RrＲｒ][TtＴｔ][EeＥｅ]{2}[NnＮｎ]|[1１][3３])(?:[TtＴｔ][HhＨｈ])?)|([FfＦｆ][IiＩｉ][RrＲｒ][SsＳｓ][TtＴｔ]|[OoＯｏ0０][NnＮｎ][EeＥｅ]|[1１](?:[SsＳｓ][TtＴｔ])?)|([SsＳｓ][EeＥｅ][CcＣｃ][OoＯｏ0０][NnＮｎ][DdＤｄ]|[TtＴｔ][WwＷｗ][OoＯｏ0０]|[2２](?:[NnＮｎ][DdＤｄ])?)|([TtＴｔ][HhＨｈ](?:[IiＩｉ][RrＲｒ][DdＤｄ]|[RrＲｒ][EeＥｅ]{2})|[3３](?:[RrＲｒ][DdＤｄ])?)|((?:[FfＦｆ][OoＯｏ0０][UuＵｕ][RrＲｒ]|4|４)(?:[TtＴｔ][HhＨｈ])?)|([FfＦｆ][IiＩｉ](?:[FfＦｆ][TtＴｔ][HhＨｈ]|[VvＶｖ][EeＥｅ])|[5５](?:[TtＴｔ][HhＨｈ])?)|((?:[SsＳｓ][IiＩｉ][XxＸｘ×]|6|６)(?:[TtＴｔ][HhＨｈ])?)|((?:[SsＳｓ][EeＥｅ][VvＶｖ][EeＥｅ][NnＮｎ]|7|７)(?:[TtＴｔ][HhＨｈ])?)|([NnＮｎ][IiＩｉ][NnＮｎ](?:[TtＴｔ][HhＨｈ]|[EeＥｅ])|[9９](?:[TtＴｔ][HhＨｈ])?)|([FfＦｆ][LlＬｌ](?:[AaＡａ][TtＴｔ]?)?|♭)|([bｂ])|([SsＳｓ](?:[HhＨｈ](?:[AaＡａ](?:[RrＲｒ][PpＰｐ]?)?)?)?|[#＃♯])|([DdＤｄ](?:[OoＯｏ0０][UuＵｕ][BbＢｂ][LlＬｌ][EeＥｅ]|[BbＢｂ][LlＬｌ])[-‑‑⁻₋﹣−˗ー－ 	 ﻿ -   　]*(?:[FfＦｆ][LlＬｌ](?:[AaＡａ][TtＴｔ]?)?|♭)|𝄫)|([DdＤｄ](?:[OoＯｏ0０][UuＵｕ][BbＢｂ][LlＬｌ][EeＥｅ]|[BbＢｂ][LlＬｌ])[-‑‑⁻₋﹣−˗ー－ 	 ﻿ -   　]*(?:[SsＳｓ](?:[HhＨｈ](?:[AaＡａ](?:[RrＲｒ][PpＰｐ]?)?)?)?|[#＃♯])|𝄪|[XxＸｘ×])|([DdＤｄ]?(?:[OoＯｏ0０][UuＵｕ][BbＢｂ][LlＬｌ][EeＥｅ]|[BbＢｂ][LlＬｌ])[-‑‑⁻₋﹣−˗ー－ 	 ﻿ -   　]*(?:[NnＮｎ][AaＡａ](?:[TtＴｔ](?:[UuＵｕ](?:[RrＲｒ](?:[AaＡａ][LlＬｌ]?)?)?)?)?|♮))|([AaＡａ]|[VvＶｖ][IiＩｉ](?![IiＩｉ])|[Ⅵⅵ])|([BＢ]|[VvＶｖ][IiＩｉ]{2}|[Ⅶⅶ])|([CcＣｃ]|[IiＩｉ](?![IiＩｉVvＶｖ])|[Ⅰⅰ])|([DdＤｄ]|[IiＩｉ]{2}(?![IiＩｉ])|[Ⅱⅱ])|([EeＥｅ]|[IiＩｉ]{3}|[Ⅲⅲ])|([FfＦｆ]|[IiＩｉ][VvＶｖ]|[Ⅳⅳ])|([GgＧｇ]|[VvＶｖ](?![IiＩｉ])|[Ⅴⅴ])|([ 	 ﻿ -   　]+)|([NnＮｎ](?:[OoＯｏ0０][NnＮｎ]?)?[-‑‑⁻₋﹣−˗ー－ 	  -   　。．，、・,.]*[CcＣｃ](?:[HhＨｈ](?:[OoＯｏ0０](?:[RrＲｒ][DdＤｄ]?)?)?)?[。．，、・,.]*|[\^])"
# )


# def chord_translate(chord_str: str, base_oct: int = 3):
#     parts = [list(filter(lambda x: x != "", e))[0] for e in REGEX.findall(chord_str)]
#     chord = pychord.Chord(parts[0])
#     if chord.on:
#         return chord.components_with_pitch(base_oct - 1)
#     else:
#         return chord.components_with_pitch(base_oct)
