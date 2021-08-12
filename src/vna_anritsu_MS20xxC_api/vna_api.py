from typing import List, Tuple, Dict
from vna_anritsu_MS20xxC_api.vna_types import *

import pyvisa
import re
import skrf as rf
import numpy as np

rm = pyvisa.ResourceManager()

def list_visa_devices() -> Tuple[str, ...]:
    return rm.list_resources()

def is_instrument_supported(identification) -> bool:
    idn = identification.split(",")
    pat = re.compile("^MS20[0-9]{2}C")
    return len(idn) > 1 and idn[0] == "Anritsu" and pat.match(idn[1]) is not None
def convert_traces_data_to_s2p(trace_data: List[np.ndarray], freq_setting: FrequencySettings):
    pass

class VNA: 
    def __init__(self, instrument_id: str):
        self.inst = rm.open_resource(instrument_id)
    
    def __del___(self):
        if self.inst is not None:
            self.inst.close()
    
    def get_identification(self) -> str:
        return self.inst.query("*IDN?")

    def get_traces_data_as_s2p(self) -> rf.Network:
        freq = rf.Frequency(1, 10, 101, 'ghz')
        s = np.random.rand(101, 2, 2) + 1j*np.random.rand(101, 2, 2)
        ntwk = rf.Network(frequency=freq, s=s, name='random values 2-port')
        return ntwk
    def set_traces_as_s2p(self) -> None:
        pass
    def set_trace_spar(self, trace_num: int, sparam: str):
        pass
    def get_trace_spar(self, trace_num: int) -> str:
        pass
    def get_trace_data(self, trace_num: int) -> np.ndarray:
        pass
    def get_trace_header(self, trace_num: int) -> Dict[str, str]:
        pass


    def get_freq_settings(self) -> FrequencySettings:
        pass
    def set_freq_settings(self, f_start, f_stop, points_num) -> None:
        pass    
