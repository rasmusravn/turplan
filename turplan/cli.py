import typer

from turplan.commands.add import add_activity, add_location, add_participant
from turplan.commands.config import config_init, config_load

app = typer.Typer(
    no_args_is_help=True,
    help="""
    Et CLI-værktøj til at planlæggeture, \n
    """,
)


app.command("config indlæs")(config_load)
app.command("config init")(config_init)
app.command("tilføj deltager")(add_participant)
app.command("tilføj aktivitet")(add_activity)
app.command("tilføj lokation")(add_location)

if __name__ == "__main__":
    app()
