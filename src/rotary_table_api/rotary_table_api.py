from typing import Dict
import serial
import serial.tools.list_ports as ser_list
from serial.tools.list_ports_common import ListPortInfo
from rotary_table_api.rotary_table_messages import *

COM_PORT_VID = 0x0483
COM_PORT_PID = 0x5740
BROADCAST_ADDRESS = 0xF
CONTROLLER_ADDRESS = 0xE

def list_com_ports() -> Dict[str, ListPortInfo]:
    ports = ser_list.comports()
    ports_dict = {}
    for port in ports:
        ports_dict[port.name] = port
    return ports_dict
def is_com_port_valid(port_info: ListPortInfo) -> bool:
    """Check if COM port is USB device with correct VID and PID"""
    if isinstance(port_info, ListPortInfo):
        if port_info.pid == COM_PORT_PID and port_info.vid == COM_PORT_VID:
            return True
    return False

class RotaryTable:
    def __init__(self, port_name: str):
        self.inst = serial.Serial(port_name)
    
    def __del___(self):
        if self.inst is not None:
            self.inst.close()
    
    def send_request(self, request: Request) -> Response:
        self.inst.write(request.to_bytes())
        resp_data = self.inst.read(REPONSE_LENGTH)
        return parse_response(resp_data)
