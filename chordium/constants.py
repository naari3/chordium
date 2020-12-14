import re

signature = r"[#b]{0,2}"
scales = r"[CDEFGAB]"
degrees = r"(VII|III|IV|VI|II|I|V)"
note = f"{scales}{signature}"
note_with_oct = f"(?P<note>{note})(?P<oct>\\d)"
space = r"[ 　]+"
degree_note = f"{degrees}{signature}"
special_notes = ["%", "=", "_", "-"]
on_chord_separator = r"(\/|on)"
chord_types = "(?![#♯b♭])(?:(?!(on))[Ma-z0-9()（）,\\-+#♯＃b♭ｂ△ΔΦφø^°])+"

root_chord = f"({note}|{'|'.join(special_notes)})"
degree_root_chord = f"({degree_note}|{'|'.join(special_notes)})"

on_chord = f"{on_chord_separator}{note}"
on_degree_chord = f"{on_chord_separator}{degree_note}"

chord_type = chord_types
chord_without_special = f"({note}({chord_types})?({on_chord_separator}{note})?)|({degree_note}({chord_types})?({on_chord_separator}{degree_note})?)"
chord_regex = re.compile(f"^({chord_without_special}|{'|'.join(special_notes)})")

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

TONE_DICT = {
    "C": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "B": 11,
}

# musthe の Scale が # を持つトーンを作りがちなのでその対策をする
# B# や G## が存在してしまう
TONE_FROM_MUSTHE = {
    "B#": "C",
    "C": "C",
    "C#": "C#",
    "Db": "Db",
    "C##": "D",
    "D": "D",
    "D#": "D#",
    "Eb": "Eb",
    "D##": "E",
    "E": "E",
    "E#": "F",
    "F": "F",
    "F#": "F#",
    "Gb": "Gb",
    "F##": "G",
    "G": "G",
    "G#": "G#",
    "Ab": "Ab",
    "G##": "A",
    "A": "A",
    "A#": "A#",
    "Bb": "Bb",
    "A##": "B",
    "B": "B",
}
MUSTHE_TONE_DICT = {}
for t, v in TONE_DICT.items():
    if not "b" in t:
        MUSTHE_TONE_DICT[f"{t}#"] = (v + 1) % 11
    MUSTHE_TONE_DICT[t] = v

INV_TONE_DICT = {v: k for k, v in TONE_DICT.items()}