from app.db.models import User
from app import db

def _test_dashboard(application, add_db_user_fixture):
    user = add_db_user_fixture

    with application.test_client(user=user) as client:
        resp = client.get('dashboard')

    assert resp.status_code == 200
    assert b'Dashboard' in resp.data


def _test_dashboard_deny(client):

    resp = client.get('dashboard', follow_redirects=True)

    assert resp.status_code == 200
    assert b'Login to Dasboard Failed' in resp.data