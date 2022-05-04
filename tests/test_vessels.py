import json

import pytest
from flask_migrate import Migrate

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))

from apis.app import create_app
from apis.models.model import db
from apis.models.vessel import vessel
from sqlalchemy import func


@pytest.fixture(scope="module")
def app():
    app = create_app(test_config=True)
    
    with app.app_context():
        db.create_all()
        Migrate(app, db)

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_get_all_vessels(app):
    """
    GIVEN an endpoint for vessel's information
    WHEN a list of all data registered is requested
    THEN check if the response is successful and returns all the vessels on db with id and code as string assigned
    """
    response = app.test_client().get('/vessel/list_vessel')
    res = json.loads(response.data.decode('utf-8')).get('vessels')
    assert response.status_code == 200
    assert len(res[0]) == 2
    assert type(res[0][1]) is str

def test_insert_clean_db(app):
    result = app.test_client().post('/vessel/insert_vessel', json={'code':'MV102'})
    assert result.get_json().get('message') == 'OK'
    assert result.status_code == 201
    with app.app_context():
        query = db.session.query(vessel.code)
        query_results = db.session.execute(query).all()
        assert query_results[0][0] == 'MV102'

def test_insert_replicated(app):
    result = app.test_client().post('/vessel/insert_vessel', json={'code':'MV102'})
    assert result.get_json().get('message') == 'FAIL'
    assert result.status_code == 409
    with app.app_context():
        query = db.session.query(func.count(vessel.code))
        query_results = db.session.execute(query).all()
        assert query_results[0][0] == 1

def test_insert_wrong_format(app):
    """
    GIVEN an endpoint for insert a new vessel
    WHEN is posted a vessel's code in wrong format
    THEN check if the response is unsuccessful with a status and message that indicates this situation and if the post request didn't have added any data to db
    """
    result = app.test_client().post('/vessels/insert_vessel', json={'code': 'MVV02'})
    assert result.get_json().get('message') == 'WRONG_FORMAT'
    assert result.status_code == 400
    with app.app_context():
        query = db.session.query(func.count(vessel.code))
        query_results = db.session.execute(query).all()
        assert query_results[0][0] == 0