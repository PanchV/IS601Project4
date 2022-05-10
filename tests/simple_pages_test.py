"""This tests the homepage"""

#22
def _test_request_main_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/about"' in response.data
    assert b'href="/welcome"' in response.data
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data

#23
def _test_request_index(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Index" in response.data

#24
def _test_request_about(client):
    """This makes the index page"""
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About" in response.data

#25
def _test_request_page1(client):
    """This makes the index page"""
    response = client.get("/welcome")
    assert response.status_code == 200
    assert b"welcome" in response.data

#26
def _test_request_page_not_found(client):
    """This makes the index page"""
    response = client.get("/page5")
    assert response.status_code == 404