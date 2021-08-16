import pytest
from rotary_table_api import rotary_table_messages as rt_msg

def test_simple_messages():
    msg = rt_msg.MessageGetStatus(0x2)
    assert msg.to_bytes() == b"\x20\xE0"

    msg = rt_msg.MessageSetHome(0x3)
    assert msg.to_bytes() == b"\x31\x97"
    
    msg = rt_msg.MessageHalt(0x5)
    assert msg.to_bytes() == b"\x52\xB9"

    msg = rt_msg.MessageDisable(0x7)
    assert msg.to_bytes() == b"\x73\x5E"

def set_rt_msg_constants():
    rt_msg.RPM_PRECISION = 0.5
    rt_msg.SPEED_MAX = 2**7
    rt_msg.RPM_MAX = rt_msg.SPEED_MAX/rt_msg.RPM_PRECISION
    rt_msg.ANGLE_FRACTION_LENGTH = 3
    rt_msg.ANGLE_PRECISION = 2**-rt_msg.ANGLE_FRACTION_LENGTH

def test_rotate_message():
    set_rt_msg_constants()
    msg = rt_msg.MessageRotate(0x2, 0, 16)
    assert msg.to_bytes() == b"\x24\x00\x00\x20\x76"
    msg = rt_msg.MessageRotate(0x3, 0.375, -16)
    assert msg.to_bytes() == b"\x34\x00\x30\xE0\xA6"
    msg = rt_msg.MessageRotate(0x3, -89.378, -16.2)
    assert msg.to_bytes() == b"\x34\x87\x50\xE0\x4E"

def test_messages_fields():
    set_rt_msg_constants()
    msg = rt_msg.MessageGetStatus(0x2)
    assert msg.address == 2
    with pytest.raises(ValueError):
        msg.address = 16

    msg = rt_msg.MessageRotate(0x2, 0, 10)
    assert msg.angle == 0
    msg.angle = 361
    assert msg.angle == 1
    msg.angle = -270
    assert msg.angle == 90
    
    msg.angle = 90.125
    assert msg.angle == 90.125
    msg.angle = 90.123
    assert msg.angle == 90.125
    msg.angle = 90.21
    assert msg.angle == 90.25

    with pytest.raises(ValueError):
        msg.rpm = 1000
    msg.rpm = 10
    assert msg.rpm == 10
    msg.rpm = -1.5
    assert msg.rpm == -1.5
    msg.rpm = -1.76
    assert msg.rpm == -2
