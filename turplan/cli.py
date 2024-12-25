import click


@click.group()
@click.version_option()
def cli():
    "CLI program til at holde styr på en kommende tur"


@cli.command(name="init")
@click.option(
    "-m",
    "--mappe",
    help="Mappe hvor projektet for den nye tur skal gemmes",
)
def first_command(mappe):
    "Command description goes here"
    click.echo(f"Følgende mappe valgt til tur: {mappe}")
