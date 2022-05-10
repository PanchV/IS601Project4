"""This makes the test configuration setup"""
# pylint: disable=redefined-outer-name
import os
import pytest
from app.db import db
from app import create_app

#8
@pytest.fixture()
def application():
    """This makes the app"""
    application = create_app()
    application.config.update({
        "TESTING": True,
    })
    yield application

#9
@pytest.fixture()
def client(application):
    """This makes the http client"""
    return application.test_client()

#10
@pytest.fixture()
def runner(application):
    """This makes the task runner"""
    return application.test_cli_runner()