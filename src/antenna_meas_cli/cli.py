from vna_anritsu_MS20xxC_api import vna

def cli():
    devices = vna.list_visa_devices()
    print(devices)

if __name__ == "__main__":
    cli()
    