import typing

import click
import uvicorn


@click.group()
def cli():
    """
    Extract Venmo transactions from a profile with one command
    """
    pass


@cli.command()
@click.option("--host", help="The output database path", default="127.0.0.1")
@click.option(
    "--port", "-o", help="The output database path", type=click.INT, default=8000
)
def serve(host: str, port: int):
    """
    Convert space-separated list of CSV files into database
    """
    uvicorn.run(None, host=host, port=port)


@cli.command()
def new_config():
    """
    Convert space-separated list of CSV files into database
    """
    pass
