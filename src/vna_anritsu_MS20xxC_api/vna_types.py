from collections import namedtuple
from typing import Final

FrequencySettings = namedtuple("FrequencySettings", ["start", "stop", "points_num"])

class SParams:
    S11: Final = "s11"
    S12: Final = "s12"
    S21: Final = "s21"
    S22: Final = "s22"

