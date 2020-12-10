from .score_objects import Chord, Base, Tie, Same, Sleep
from chordium import ChordiumException

from typing import List, Iterable, Optional, Tuple, NamedTuple
from itertools import chain

import random
import pretty_midi


class BeatLength(NamedTuple):
    kind: Base
    length: int


class ScoreProgression(object):
    def __init__(self, bpm: int = 120, score_object_lists: List[List[Base]] = []):
        self.bpm = bpm
        self.score_object_lists = score_object_lists
        self.progress = 0

    def __repr__(self):
        return f"<ScoreProgression score: {self.show_progress()} >"

    def show_progress(self):
        return " | ".join(
            [
                " ".join(list(map(lambda c: c._show_progress(), score_objects)))
                for score_objects in self.score_object_lists
            ]
        )

    def to_notes(self, scale: int) -> List[pretty_midi.Note]:
        notes = []
        beat_length_list_list = [
            self._bar_to_beat_length_list(score_object_list)
            for score_object_list in self.score_object_lists
        ]
        beat_length_list = self._merge_beat_length_list(beat_length_list_list)
        bpm_multiplexer = 60 / self.bpm
        current_position = 0
        for beat_length in beat_length_list:
            if isinstance(beat_length.kind, Chord):
                for note in beat_length.kind.to_notes(scale):
                    note_number = pretty_midi.note_name_to_number(note)
                    note = pretty_midi.Note(
                        velocity=100,
                        pitch=note_number,
                        start=current_position + random.random() * 0.03,
                        end=current_position + beat_length.length * bpm_multiplexer,
                    )
                    notes.append(note)
            current_position += beat_length.length * bpm_multiplexer
            if current_position * 44100 * 16 * 2 / 8 > 8388608:
                raise ChordiumException("長すぎます！")

        return notes

    def _bar_to_beat_length_list(
        self, bar: List[Base], beat: int = 4
    ) -> List[BeatLength]:
        beat_length_list = []
        length = len(bar)
        if length == 1:
            beat_length_list.append(BeatLength(bar[0], 4))
        elif beat / length >= 2:  # 均等に埋める
            timing = beat / length
            for song_obj in bar:
                beat_length_list.append(BeatLength(song_obj, timing))
        elif length > beat and length <= beat * 2:  # 8分で埋める
            remain = 4 - (length - 1) * 0.5
            for song_obj in bar[:-1]:
                beat_length_list.append(BeatLength(song_obj, 0.5))
            beat_length_list.append(BeatLength(bar[-1], remain))
        elif length > beat * 2:  # 16分で埋める
            remain = 4 - (length - 1) * 0.25
            for song_obj in bar[:-1]:
                beat_length_list.append(BeatLength(song_obj, 0.25))
            beat_length_list.append(BeatLength(bar[-1], remain))
        else:  # 4分で埋める
            remain = 4 - (length - 1) * 1
            for song_obj in bar[:-1]:
                beat_length_list.append(BeatLength(song_obj, 1))
            beat_length_list.append(BeatLength(bar[-1], remain))
        return beat_length_list

    def _merge_beat_length_list(
        self, beat_length_list_list: List[List[BeatLength]]
    ) -> List[BeatLength]:  # fucking args name
        beat_length_list = chain.from_iterable(beat_length_list_list)
        new_beat_length_list = []
        for beat_length in beat_length_list:
            if isinstance(beat_length.kind, Same):
                same_beat_length = BeatLength(
                    new_beat_length_list[-1].kind, beat_length.length
                )
                new_beat_length_list.append(same_beat_length)
            elif isinstance(beat_length[0], Tie):
                tied_beat_length = BeatLength(
                    new_beat_length_list[-1].kind,
                    new_beat_length_list[-1].length + beat_length.length,
                )
                new_beat_length_list[-1] = tied_beat_length
            else:
                new_beat_length_list.append(beat_length)
        return new_beat_length_list