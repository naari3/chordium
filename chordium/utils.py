import numpy as np
import pychord


def f64le_to_s32le(data):
    shifted = data * (2 ** 31 - 1)  # Data ranges from -1.0 to 1.0
    ints = shifted.astype(np.int32)
    return ints


def scale_to_int(scale: str):
    try:
        scale = int(scale, base=10)
    except ValueError:
        scale = pychord.constants.NOTE_VAL_DICT[scale]
    return scale