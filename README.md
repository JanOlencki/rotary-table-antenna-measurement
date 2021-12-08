# Usage
Repo contains rotary table API, VNA (Anritsu MS200xxC) API, simple command line interface and example script. These code are created to automate antenna radiation pattern measurements using custom measurement system, which documentation and source code will be published in the future.
## CLI
CLI may be used by running commands in *src* directory. Example commands listed below show help for different CLI functions
```
python -m antenna_meas_cli.cli --help
python -m antenna_meas_cli.cli meas --help
python -m antenna_meas_cli.cli list-devices --help
python -m antenna_meas_cli.cli vna-meas --help
```
## Example script
Example script (*src/example.py*) used rotary table's and VNA's APIs to make simple measurement of antenna radiation pattern. This script may be ran by command below executed in *src* directory.
```
python example.py
```
## Software required to install
- Python *v3.9*
- NI-VISA driver *v21.0* (https://www.ni.com/pl-pl/support/downloads/drivers/download.ni-visa.html#409839
## Python dependencies
- pyvisa *v1.11*
- scikit-rf *v0.19*
- click *v8.0*
- crc8 *v0.1*
- pyserial *v3.5*
# Development
Repo contains config files (*launch.json* and *settings.json* in *.vscode* directory) for Visual Studio Code.
## Development dependencies
- pytest *v6.2*