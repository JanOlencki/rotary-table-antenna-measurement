from vna_anritsu_MS20xxC_api import vna_api

def test_checking_device_indentification():
    assert vna_api.is_instrument_supported("Anritsu,MS2028C/10/2,62011032,1.23") == True
    assert vna_api.is_instrument_supported("Anritsu,MS102333C/10/2,62011032,1.23") == False
    assert vna_api.is_instrument_supported("Anritsu,te") == False
    assert vna_api.is_instrument_supported("Anritsu") == False
    assert vna_api.is_instrument_supported("ee") == False
    assert vna_api.is_instrument_supported("") == False


