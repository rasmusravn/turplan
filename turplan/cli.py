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
    "Denne commando bruges til at starte et projekt. En passende mappestruktur oprettes"
    click.echo(f"Følgende mappe valgt til tur: {mappe}")
