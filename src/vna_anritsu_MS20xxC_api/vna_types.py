from collections import namedtuple
from typing import Final

class FrequencySettings:
    start: int = None
    stop: int = None
    points_num: int = None
    

class SParam:
    S11: Final = "s11"
    S12: Final = "s12"
    S21: Final = "s21"
    S22: Final = "s22"

class Domain:
    FREQ: Final = "FREQ"
    TIME: Final = "TIME"
    DISTANCE: Final = "DIST"
    FREQ_GATE: Final = "FGT"

