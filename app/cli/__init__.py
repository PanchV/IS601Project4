import click
from flask.cli import with_appcontext
from app.db import db
from app.db import make_db_directory

@click.command(name='create-db')
@with_appcontext
def create_database():
    make_db_directory()
    db.create_all()