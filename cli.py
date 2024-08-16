import typer
import alembic.config
from seeders.initial_seeders import initial_seeders

app = typer.Typer()


@app.command()
def initial_data():
    initial_seeders()


@app.command()
def initial_migrate():
    alembic_args = ["-c", "alembic.ini", "downgrade", "base"]
    alembic.config.main(argv=alembic_args)
    alembic_args = ["-c", "alembic.ini", "upgrade", "head"]
    alembic.config.main(argv=alembic_args)
    initial_seeders()


if __name__ == "__main__":
    app()
