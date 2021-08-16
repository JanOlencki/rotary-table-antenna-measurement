import pyvisa
import time
from vna_anritsu_MS20xxC_api import vna_api
from vna_anritsu_MS20xxC_api.vna_types import FrequencySettings, SParam

def test_listing_resources():
    rm = pyvisa.ResourceManager()
    devices = vna_api.list_visa_instruments(rm)
    assert len(devices) > 0
    assert vna_api.find_vna_instrument_by_idn(rm) is not None

def get_vna():
    rm = pyvisa.ResourceManager()
    id = vna_api.find_vna_instrument_by_idn(rm)
    return vna_api.VNA(rm, id)
def wait_between_changes():
    time.sleep(3)

def test_freq_changing():
    vna = get_vna()
    settings = [vna.get_freq_settings(), FrequencySettings(100E3, 2E9, 1000), FrequencySettings(200E3, 3E9, 2000), None]
    settings[-1] = settings[0]
    for setting in settings:
        assert setting is not None
        vna.set_freq_settings(*setting)
        assert vna.get_freq_settings() == setting
        wait_between_changes()

def test_traces_count_changing():
    vna = get_vna()
    traces_count = vna.get_traces_count()
    vna.set_traces_count(2)
    assert vna.get_traces_count() == 2
    time.sleep(3)
    vna.set_traces_count(traces_count)
    assert vna.get_traces_count() == traces_count

def test_trace_spar():
    vna = get_vna()
    trace = 1
    spar = vna.get_trace_spar(trace)
    vna.set_trace_spar(trace, SParam.S11)
    assert vna.get_trace_spar(trace) == SParam.S11
    time.sleep(3)
    vna.set_trace_spar(trace, spar)
    assert vna.get_trace_spar(trace) == spar
