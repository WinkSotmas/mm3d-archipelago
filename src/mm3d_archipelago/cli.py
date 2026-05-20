import click
import time
from .citra import launch_citra
from .archipelago_client import ArchipelagoClient


@click.group()
def cli():
    """MM3D Archipelago helper CLI."""
    pass


@cli.command()
@click.option('--citra-path', '-c', default='citra-qt', help='Path to Citra executable')
@click.argument('rom', type=click.Path(exists=True))
def start(citra_path, rom):
    """Launch Citra with the given ROM."""
    launch_citra(citra_path, rom)


@cli.command()
@click.option('--server', '-s', help='Archipelago server', required=True)
@click.option('--slot', '-l', help='Player slot name', required=True)
def connect(server, slot):
    """Connect to an Archipelago server and listen for incoming items."""
    client = ArchipelagoClient(server, slot)

    def on_item(location_id: int, item_id: int):
        click.echo(f"[item] received location={location_id} item={item_id}")

    client.set_item_callback(on_item)
    client.connect()

    click.echo('Connected; listening for items. Press Ctrl+C to exit.')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        click.echo('Disconnecting...')
        client.disconnect()


@cli.command(name='simulate-item')
@click.option('--server', '-s', help='Archipelago server', required=False)
@click.option('--slot', '-l', help='Player slot name', required=False)
@click.argument('location_id', type=int)
@click.argument('item_id', type=int)
def simulate_item(server, slot, location_id, item_id):
    """Simulate receiving an item (for local testing)."""
    client = ArchipelagoClient(server or 'local', slot or 'test')
    # no real connection required for simulation
    client.set_item_callback(lambda loc, it: click.echo(f"[sim] item={it} at loc={loc}"))
    client.simulate_receive(location_id, item_id)


if __name__ == '__main__':
    cli()
