import pyvisa
import time
from vna_anritsu_MS20xxC_api import vna_api
from vna_anritsu_MS20xxC_api.vna_types import FrequencySettings, SParam

def test_listing_resources():
    rm = pyvisa.ResourceManager()
    devices = vna_api.list_visa_instruments(rm)
    assert len(devices) > 0
    assert vna_api.find_vna_instrument_id(rm) is not None

def get_vna():
    rm = pyvisa.ResourceManager()
    id = vna_api.find_vna_instrument_id(rm)
    return vna_api.VNA(rm, id)

def test_freq_changing():
    vna = get_vna()
    settings_before = vna.get_freq_settings()
    assert settings_before is not None
    settings = FrequencySettings(100E3, 2E9, 1000)
    vna.set_freq_settings(*settings)
    assert vna.get_freq_settings() == settings
    time.sleep(3)
    vna.set_freq_settings(*settings_before)
    assert vna.get_freq_settings() == settings_before

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
