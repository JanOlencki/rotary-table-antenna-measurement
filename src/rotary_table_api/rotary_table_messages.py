from abc import ABC, abstractmethod
from typing import Literal

import crc8

def round_to(val: float, precision: float):
    if val % precision < precision/2:
        val -= val % precision
    else:
        val += precision - val % precision
    return val

ADDRESS_LENGTH = 4
class Message(ABC):
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
        cont = self.get_content()
        crc = self.get_CRC()
        return self.get_content() + self.get_CRC()

    def __eq__(self, other):
        if isinstance(other, Message):
            return self.get_content() == other.get_content()
        return False

class MessageGetStatus(Message):
    def get_command(self) -> int:
        return 0

class MessageSetHome(Message):
    def get_command(self) -> int:
        return 1

class MessageHalt(Message):
    def get_command(self) -> int:
        return 2
        
class MessageDisable(Message):
    def get_command(self) -> int:
        return 3

RPM_PRECISION = 0.5
SPEED_MAX = 2**7
RPM_MAX = SPEED_MAX/RPM_PRECISION
ANGLE_FRACTION_LENGTH = 3
ANGLE_PRECISION = 2**-ANGLE_FRACTION_LENGTH
class MessageRotate(Message):
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
        angle = int(self.angle) << 7
        angle |= int((self.angle % 1)/ANGLE_PRECISION) << (8-1-ANGLE_FRACTION_LENGTH)
        angle_b = angle.to_bytes(2, byteorder="big")
        rpm_b = int(self.rpm/RPM_PRECISION).to_bytes(1, byteorder="big", signed=True)
        return angle_b + rpm_b
        
