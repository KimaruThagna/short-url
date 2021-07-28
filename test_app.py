import pytest
from urlapp.models import UrlRecord
from urlapp import init_app, db
 
@pytest.fixture(scope='module')
def new_record():
    record = UrlRecord(url="https://looker.com", 
                  shortcode='Lk95r4')
    return record

@pytest.fixture(scope='module')
def test_client():
    flask_app = init_app('flask_test.cfg')
    testing_client = flask_app.test_client()
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client  # this is where the testing happens!
    ctx.pop()

@pytest.fixture(scope='module')
def init_db():
    # Create the database and the database table
    db.create_all()
 
    # Insert user data
    record = UrlRecord(url="https://looker.com", 
                  shortcode='Lk95r4')
    db.session.add(record)
    db.session.commit()
    yield db
    
    db.drop_all()
    
def test_url_record(new_record):
    assert new_record.shortcode == 'Lk95r4'
    assert isinstance(new_record, UrlRecord)
    
def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data
    
        
def test_stats(test_client):
    response = test_client.get('/url/Lk95r4/stats')
    assert response.status_code == 200
        
def test_valid_url(test_client):
    response = test_client.get('/url/Lk95r4')
    assert response.status_code == 302 # redirect
        
def test_invalid_url(test_client):
    response = test_client.get('/url/fghjkfghjkghjk74852')
    assert response.status_code == 404


def test_record_exists(init_db):
    assert len(UrlRecord.query.all()) == 1
    record = UrlRecord.query.first()
    assert record.access_count == 0
        
def test_access_count_update():
    record = UrlRecord.query.first()
    record.update_access_count()
    assert record.access_count == 1
    