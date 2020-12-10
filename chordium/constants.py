import re

signature = r"[#b]{0,2}"
scales = r"[CDEFGAB]"
degrees = r"(VII|III|IV|VI|II|I|V)"
note = f"{scales}{signature}"
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
chord_regex = re.compile(
    f"^(({note}({chord_types})?({on_chord_separator}{note})?)|({degree_note}({chord_types})?({on_chord_separator}{degree_note})?)|{'|'.join(special_notes)})"
)

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