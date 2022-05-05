from flask import Blueprint, cli
from flask_sqlalchemy import SQLAlchemy
from app import config

import logging
import os

db = SQLAlchemy()

database = Blueprint('database', __name__,)

@database.cli.command('create')
def init_db():
    db.create_all()


def make_db_directory():
    log = logging.getLogger("misc_debug")
    root = current_app.config["BASE_DIR"]
    db_dir = os.path.join(root, '..', current_app.config["DB_DIR"])
    if not os.path.exists(db_dir):
        log.debug("[%s] Making DB Directory %s", current_app.env, db_dir)
        os.mkdir(db_dir)