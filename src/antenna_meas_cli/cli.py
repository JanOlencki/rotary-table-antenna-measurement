from vna_anritsu_MS20xxC_api import vna_api

def cli():
    devices = vna_api.list_visa_devices()
    vna = vna_api.VNA(devices[0])
    print(devices)
    print(vna)


if __name__ == "__main__":
    cli()
    