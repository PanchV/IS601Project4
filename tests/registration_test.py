"""This test authorization pages"""
from app.db.models import User
from app import db

def _register_user_test(client):
    """ POST to /register """
    new_email = 'panchpandu11@gmail.com'
    new_password = 'password'
    assert not User.query.filter_by(email=new_email).first()

    data = {
        'email' : new_email,
        'password' : new_password,
        'confirm' : new_password
    }
    resp = client.post('register', data=data)

    assert resp.status_code == 302
    new_user = User.query.filter_by(email=new_email).first()
    assert new_user.email == new_email

    db.session.delete(new_user)