from typing import Tuple
import pyvisa

rm = pyvisa.ResourceManager()

def list_visa_devices() -> Tuple[str, ...]:
    return rm.list_resources()
