from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from app import config
import os

db = SQLAlchemy()

database = Blueprint('database', __name__,)


def create_db_path():
    root = config.Config.BASE_DIR
    db_dir = os.path.join(root, '..', config.Config.DB_DIR)
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)

@database.cli.command('create')
def init_db():
    create_db_path()
    db.create_all()

@database.before_app_first_request
def db_path_if_not_exist():
    create_db_path()
    db.create_all()