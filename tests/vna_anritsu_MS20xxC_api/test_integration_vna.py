import sys
print(sys.path)

from vna_anritsu_MS20xxC_api import vna

def test_listing_resources():
    devices = vna.list_visa_devices()
    assert len(devices)
