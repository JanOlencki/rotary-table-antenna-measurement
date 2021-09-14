import pyvisa
import click
from vna_anritsu_MS20xxC_api import vna_api
from rotary_table_api import rotary_table_api as rt_api
from rotary_table_api import rotary_table_messages as rt_msg

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

@click.command()
@click.option("--rt-port", required=True, help="Rotary table controller COM port")
@click.option("--rt-id", required=True, type=int, help="Rotary table ID")
def meas(rt_port, rt_id):
    rt = rt_api.RotaryTable(rt_port)
    resp = rt.send_request(rt_msg.RequestGetConverterStatus(rt_api.CONTROLLER_ADDRESS))
    if not resp.is_valid or not isinstance(resp, rt_msg.ResponseConverterStatus):
        raise IOError("Unexpected or incorrect response")
    click.echo("Controller voltage = ", nl=False)
    volt_fg = "green" if resp.is_voltage_OK else "red"
    click.secho(f"{resp.voltage:2.2f} V", fg=volt_fg)

    resp = rt.send_request(rt_msg.RequestHalt(rt_id))
    resp = rt.send_request(rt_msg.RequestSetHome(rt_id))

@click.group(name="antenna-meas")
def cli():
    pass
cli.add_command(list_devices)
cli.add_command(meas)
if __name__ == "__main__":
    cli()
    