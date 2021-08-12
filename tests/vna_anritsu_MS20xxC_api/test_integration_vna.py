from vna_anritsu_MS20xxC_api import vna_api

def test_listing_resources():
    devices = vna_api.list_visa_devices()
    assert len(devices)
