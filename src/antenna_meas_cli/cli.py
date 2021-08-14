import pyvisa
from vna_anritsu_MS20xxC_api import vna_api

def cli():
    rm = pyvisa.ResourceManager()
    id = vna_api.find_vna_instrument_idn(rm)
    vna = vna_api.VNA(rm, id)
    vna.set_traces_as_s2p()
    vna.set_freq_settings(20E3, 5E9, 20)
    print(vna.get_trace_data(1))
    print(vna.get_trace_freq_data(1))


if __name__ == "__main__":
    cli()
    