import pytest
from click.testing import CliRunner

from beaconator import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_main_succeeds(runner: CliRunner):
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
