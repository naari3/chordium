import numpy as np


def f64le_to_s32le(data):
    shifted = data * (2 ** 31 - 1)  # Data ranges from -1.0 to 1.0
    ints = shifted.astype(np.int32)
    return ints
