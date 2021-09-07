import pyvisa
import click
from vna_anritsu_MS20xxC_api import vna_api
from rotary_table_api import rotary_table_api as rt_api

@click.command()
def list_devices():
    rm = pyvisa.ResourceManager()
    click.secho("# Note that not all ports may be listed")
    click.secho("# VISA instruments", bold=True)
    instruments = vna_api.list_visa_instruments(rm)
    for inst_name in instruments:
        idn = vna_api.get_instrument_idn(rm, inst_name)
        click.echo(inst_name + "\t", nl=False)
        if vna_api.is_instrument_supported(idn):
            click.secho(idn, fg="green")
        else:
            click.echo(idn)

    click.secho("# Rotary tables", bold=True)
    for port_name, port_info in rt_api.list_com_ports().items():
        if rt_api.is_com_port_valid(port_info):
            click.secho(port_name, fg="green")
        else:
            click.echo(port_name)

@click.group(name="antenna-meas")
def cli():
    pass
cli.add_command(list_devices)
if __name__ == "__main__":
    cli()
    