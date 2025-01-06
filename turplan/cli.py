import typer

from turplan import planning

app = typer.Typer(
    no_args_is_help=True,
    help="""
    Et CLI-værktøj til at planlæggeture, \n
    """,
)


app.add_typer(planning.app, name="plan")

if __name__ == "__main__":
    app()
