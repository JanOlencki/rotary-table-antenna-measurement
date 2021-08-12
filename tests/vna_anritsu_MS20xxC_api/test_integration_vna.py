from vna_anritsu_MS20xxC_api import vna_api

def test_listing_resources():
    devices = vna_api.list_visa_devices()
    assert len(devices) > 0
    assert len(filter(vna_api.is_instrument_supported, devices)) > 0

def get_inst_idn():
    devices = vna_api.list_visa_devices()
    for dev in devices:
        if vna_api.is_instrument_supported(dev):
            return dev

vna = vna_api.VNA(get_inst_idn())
def test_freq_changing():
    settings = vna.get_freq_settings()
    vna.set_freq_settings()
