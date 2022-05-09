from app.db.models import User
from app import db

def _login_test(client, add_db_user_fixture):

    resp = client.post('login', follow_redirects=True,
            data=data)

    data = {
        'email' : EMAIL,
        'password' : PASSWORD
    }

    assert resp.status_code == 200
    assert b'Login Successful' in resp.data