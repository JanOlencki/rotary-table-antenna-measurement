from typing import Tuple
import pyvisa
import re

rm = pyvisa.ResourceManager()

def list_visa_devices() -> Tuple[str, ...]:
    return rm.list_resources()

def is_instrument_supported(identification) -> bool:
    idn = identification.split(",")
    pat = re.compile("^MS20[0-9]{2}C")
    return len(idn) > 1 and idn[0] == "Anritsu" and pat.match(idn[1]) is not None

class VNA: 
    def __init__(self, instrument_id: str):
        self.inst = rm.open_resource(instrument_id)
    
    def __del___(self):
        if self.inst is not None:
            self.inst.close()
    
    def get_identification(self) -> str:
        return self.inst.query("*IDN?")
    
