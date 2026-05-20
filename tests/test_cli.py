from click.testing import CliRunner
from mm3d_archipelago import cli


def test_simulate_item_cli_outputs_expected():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['simulate-item', '10', '20'])
    assert result.exit_code == 0
    assert 'item=20' in result.output
