#tests/test_backend_api.py
from fastapi.testclient import TestClient
from API.main import app

client = TestClient(app)

def test_root():
    response = client.get('/')
    assert response.status_code == 200 

def test_read():
    response = client.get('/')
    assert response.status_code == 200 
'''
def test_insert_routes():
    json_obj = {'text':'This is an exemple for the test'}
    response = client.post('/insert/', json=json_obj)
    assert response.status_code == 200

def test_insert_quote():
    json_obj = {'text':'This is an exemple for the test'}
    response = client.post('/insert/', json=json_obj)
    print(json_obj)
    print(response)
    assert response.body == json_obj
'''