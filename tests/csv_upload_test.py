def _upload_songs_test(application, add_db_user_fixture):
    root = config.Config.BASE_DIR
    filename = 'transactions.csv'
    filepath = root + '/../tests/' + filename
    user = add_db_user_fixture
    upload_folder = config.Config.UPLOAD_FOLDER
    upload_file = os.path.join(upload_folder, filename)
    if os.path.exists(upload_file):
        os.remove(upload_file)
    assert resp.status_code == 302
    assert db.session.query(Song).count() == 1
    assert os.path.exists(upload_file)
    os.remove(upload_file)


def _upload_songs_deny_test(client):
    resp = client.get('transactions/upload', follow_redirects=True)
    assert b'Login Failed' in resp.data
    root = config.Config.BASE_DIR
    filename = 'transactions.csv'
    filepath = root + '/../tests/' + filename
    with open(filepath, '/../tests/') as file:
        data = {
            'file': (file, filename),
        }
        resp = client.post('songs/upload', follow_redirects=True, data=data)
    assert resp.status_code == 200