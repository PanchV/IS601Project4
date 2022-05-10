import datetime
import re
import pytest

@pytest.fixture()
def resp(client):
    """ get home/index page """
    return client.get("/")

#19
def _navigation_bar_test(resp):
    user = add_db_user_fixture
    with application.test_client(user=user) as client:
        resp = client.get('/')
    assert resp.status_code == 200

#20
def _navigation_bar_fail_test(client):
    user = add_db_user_fixture
    with application.test_client(user=user) as client:
        resp = client.get('not_a_page')
    assert resp.status_code == 404