from chordium.exceptions import ChordiumException
from chordium.models import ScoreProgression
from .score_objects import Base, Chord, Same, Sleep, Tie

import re
from typing import List, Tuple, Optional

signature = r"[#b]{0,2}"
scales = r"[CDEFGAB]"
degrees = r"(VII|III|IV|VI|II|I|V)"
note = f"{scales}{signature}"
space = r"[ 　]+"
degree_note = f"{degrees}{signature}"
special_notes = ["%", "=", "_", "-"]
on_chord_separator = r"(\/|on)"
chord_types = "(?![#♯b♭])(?:(?!(on|l))[Ma-z0-9()（）,\\-+#♯＃b♭ｂ△ΔΦφø])+"

root_chord = f"({note}|{'|'.join(special_notes)})"
degree_root_chord = f"({degree_note}|{'|'.join(special_notes)})"

on_chord = f"{on_chord_separator}{note}"
on_degree_chord = f"{on_chord_separator}{degree_note}"

chord_type = chord_types
chord_regex = re.compile(
    f"^(({note}({chord_types})?({on_chord_separator}{note})?)|({degree_note}({chord_types})?({on_chord_separator}{degree_note})?)|{'|'.join(special_notes)})"
)


class ScoreParser(object):
    """
    parse strings and return score objects
    """

    def parse(self, input: str, bpm: int) -> ScoreProgression:
        score_objects = self._parse(input)
        score_progression = ScoreProgression(bpm, score_objects)
        return score_progression

    def _parse(self, input: str) -> List[List[Base]]:
        score_objets_list = []
        bar_strs = input.split("|")
        for bar_str in bar_strs:
            score_objects = []
            while bar_str.strip() != "":
                next_input, score_object = self.tokenize(bar_str.strip())
                if score_object is None:
                    if next_input.strip():
                        raise ChordiumException(
                            f'Can\'t parse!: "{bar_str}" in "{input}"'
                        )
                    break
                score_objects.append(score_object)
                bar_str = next_input
            score_objets_list.append(score_objects)

        return score_objets_list

    def tokenize(self, input: str) -> Tuple[str, Optional[Base]]:
        result = chord_regex.match(input)
        if result is None:
            return (input, None)
        chord_str = result[0]
        will_tokenize = result.span()[1]
        if chord_str == "%":
            return (input[will_tokenize:], Same())
        elif chord_str == "=":
            return (input[will_tokenize:], Tie())
        elif chord_str == "_" or chord_str == "-":
            return (input[will_tokenize:], Sleep())
        else:
            return (input[will_tokenize:], Chord(chord_str))
