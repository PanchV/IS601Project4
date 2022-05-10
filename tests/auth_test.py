"""This test the homepage"""

#1
def _test_request_login_link(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/login"' in response.data

#2
def _test_request_register_link(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/register"' in response.data

#3
def _test_auth_page_dashboard(client):
    """This makes the index page"""
    response = client.get("/dashboard")
    assert response.status_code == 200

#4
def _test_auth_page_register(client):
    """This makes the index page"""
    response = client.get("/register")
    assert response.status_code == 200

#5
def _test_auth_page_login(client):
    """This makes the index page"""
    response = client.get("/login")
    assert response.status_code == 200