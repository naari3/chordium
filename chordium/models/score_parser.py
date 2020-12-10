from chordium.exceptions import ChordiumException
from chordium.models import ScoreProgression
from .score_objects import Base, Chord, Same, Sleep, Tie
from chordium.constants import chord_regex

import re
from typing import List, Tuple, Optional


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
            if len(score_objects) == 0:
                score_objects.append(Sleep())
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
