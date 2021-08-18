from abc import ABC, abstractmethod
from typing import Type

import crc8

def round_to(val: float, precision: float):
    if val % precision < precision/2:
        val -= val % precision
    else:
        val += precision - val % precision
    return val

ADDRESS_LENGTH = 4
class Request(ABC):
    def __init__(self, address: int):
        self.address = address
    @property
    def address(self) -> int:
        return self.__address
    @address.setter
    def address(self, address: int):
        if address > 2**ADDRESS_LENGTH-1:
            raise ValueError("Rotary table message address must be lower than 16.")
        else:
            self.__address = address

    @abstractmethod
    def get_command(self) -> int:
        raise NotImplementedError("Method get_command() must be overrided.")
    def get_body(self) -> bytes:
        return bytes(0)
    def get_content(self) -> bytes:
        header = self.address << (8-ADDRESS_LENGTH) | self.get_command()
        return header.to_bytes(1, byteorder="big") + self.get_body()
    def get_CRC(self) -> bytes:
        hash = crc8.crc8()
        hash.update(self.get_content())
        return hash.digest()
    def to_bytes(self) -> bytes:
        return self.get_content() + self.get_CRC()

    def __eq__(self, other):
        if isinstance(other, Request):
            return self.get_content() == other.get_content()
        return False

class RequestGetStatus(Request):
    def get_command(self) -> int:
        return 0

class RequestSetHome(Request):
    def get_command(self) -> int:
        return 1

class RequestHalt(Request):
    def get_command(self) -> int:
        return 2
        
class RequestDisable(Request):
    def get_command(self) -> int:
        return 3

RPM_PRECISION = 0.5
SPEED_MAX = 2**7
RPM_MAX = SPEED_MAX/RPM_PRECISION
ANGLE_FRACTION_LENGTH = 7
ANGLE_PRECISION = 2**-3
def rpm_to_bytes(rpm: float) -> bytes:
    return int(rpm/RPM_PRECISION).to_bytes(1, byteorder="big", signed=True)
def rpm_from_bytes(data: bytes) -> float:
    if len(data) != 1:
        raise ValueError("rpm_from_bytes() argument must has length = 1")
    return int.from_bytes(data, byteorder="big", signed=True)*RPM_PRECISION
def angle_to_bytes(angle: float) -> bytes:
    angle_fp = int(angle * 2**ANGLE_FRACTION_LENGTH)
    return angle_fp.to_bytes(2, byteorder="big")
def angle_from_bytes(data: bytes) -> float:
    if len(data) != 2:
        raise ValueError("angle_from_bytes() argument must has length = 2")
    return int.from_bytes(data, byteorder="big") * 2**-ANGLE_FRACTION_LENGTH

class RequestRotate(Request):
    def __init__(self, address: int, angle: float, rpm: float):
        self.address = address
        self.rpm = rpm
        self.angle = angle
    
    @property
    def rpm(self) -> float:
        return self.__rpm
    @rpm.setter
    def rpm(self, rpm: float):
        if abs(rpm) > RPM_MAX:
            raise ValueError(f"Rotary table message rpm must be between {-RPM_MAX} and {RPM_MAX} .")
        self.__rpm = round_to(rpm, RPM_PRECISION)

    @property
    def angle(self) -> float:
        return self.__angle
    @angle.setter
    def angle(self, angle: float):
        angle = angle % 360
        self.__angle = round_to(angle, ANGLE_PRECISION)

    def get_command(self) -> int:
        return 4
    def get_body(self) -> bytes:
        return angle_to_bytes(self.angle) + rpm_to_bytes(self.rpm)

REPONSE_LENGTH = 8
class Response():
    def __init__(self, data: bytes):
        self.__data = data

    @property
    def data(self) -> bytes:
        return self.__data
    
    @property
    def address(self) -> int:
        if len(self.data) < 1:
            return None
        return int(self.data[0]) >> ADDRESS_LENGTH
    
    @property
    def response_header(self) -> int:
        if len(self.data) < 1:
            return None
        return int(self.data[0]) & (2**ADDRESS_LENGTH-1)
    
    def calc_CRC(self) -> bytes:
        hash = crc8.crc8()
        hash.update(self.data[:-1])
        return hash.digest()

    @property
    def is_valid(self) -> bool:
        return len(self.data) == REPONSE_LENGTH and self.calc_CRC() == self.data[-1:]       

    def __eq__(self, other):
        if isinstance(other, Response):
            return self.data == other.data
        return False

IS_VOLTAGE_OK_MASK = 0b1
IS_MOTOR_OK_MASK = 0b1
IS_ROTATING_MASK = 0b1<<1
IS_ENABLED_MASK = 0b1<<2
IS_CRC_VALID_MASK = 0b1<<3
VOLTAGE_FRACTION_LENGTH = 4
class ResponseMotorStatus(Response):
    @property
    def status(self) -> int:
        return self.data[1]
    @property
    def is_motor_OK(self) -> bool:
        return (self.status & IS_MOTOR_OK_MASK) > 0      
    @property
    def is_rotating(self) -> bool:
        return (self.status & IS_ROTATING_MASK) > 0  
    @property
    def is_enabled(self) -> bool:
        return (self.status & IS_ENABLED_MASK) > 0     
    @property
    def is_crc_valid(self) -> bool:
        return (self.status & IS_CRC_VALID_MASK) > 0

    @property
    def current_angle(self) -> float:
        return angle_from_bytes(self.data[2:4])
    @property
    def target_angle(self) -> float:
        return angle_from_bytes(self.data[4:6])
    @property
    def rpm(self) -> float:
        return rpm_from_bytes(self.data[6:7])
    
class ResponseConverterStatus(Response):
    @property
    def status(self) -> int:
        return self.data[1]
    
    @property
    def is_voltage_OK(self) -> bool:
        return (self.status & IS_VOLTAGE_OK_MASK) > 0
    
    @property
    def voltage(self) -> float:
        return self.data[2] * 2**-VOLTAGE_FRACTION_LENGTH
    
    @property
    def reserved_data(self) -> bytes:
        return self.data[3:-1]

def parse_response(data: bytes) -> Type[Response]:
    resp = Response(data)
    if resp.response_header == 0xE:
        return ResponseConverterStatus(data)
    elif resp.response_header == 0xF:
        return ResponseMotorStatus(data)
    return resp