import click
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
    """Connect to an Archipelago server (stub)."""
    client = ArchipelagoClient(server, slot)
    client.connect()
    click.echo('Connected (stub)')


if __name__ == '__main__':
    cli()
