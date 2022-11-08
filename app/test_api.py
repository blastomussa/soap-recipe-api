# to be used with pytest
from fastapi.testclient import TestClient
from requests_toolbelt.multipart.encoder import MultipartEncoder
from requests import post

# required to find all packages in app for pytest; otherwise ModuleImport Error
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from .main import app

client = TestClient(app)

BASE_URL = "http://127.0.0.1"

# TEST ADMIN CREATED AND DELETED IN CONFTEST.PY WITH PYMONGO
TEST_USER = 'johndoe'
TEST_PW = 'secret'

def get_auth_header():
    mp_encoder = MultipartEncoder(
            fields={
                'username': TEST_USER,
                'password': TEST_PW
            }
    )
    response = post(f"{BASE_URL}/token",data=mp_encoder, headers={'Content-Type': mp_encoder.content_type})
    response_json = response.json()
    token = response_json['access_token']
    header = {
        'Authorization': f"Bearer {token}",
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    return header


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        'version': '0.0.2',
        'author': 'Joe Courtney',
        'description': 'REST API to calculate soap recipes.',
        'language': 'Python 3.10.7',
        'framework': 'FastAPI',
        'repository': 'https://github.com/blastomussa/soap-recipe-api'
    }


def test_read_oils():
    response = client.get("/oils")
    assert response.status_code == 200


def test_read_recipes():
    response = client.get("/recipes")
    assert response.status_code == 200


def test_read_users():
    response = client.get("/users", headers=get_auth_header())
    assert response.status_code == 200


def test_read_user():
    response = client.get("/users/0", headers=get_auth_header()) #test users create at _id: 0 in pytest conguration phase
    assert response.status_code == 200


def test_get_token():
    mp_encoder = MultipartEncoder(
            fields={
                'username': TEST_USER,
                'password': TEST_PW
            }
    )
    response = post(f"{BASE_URL}/token",data=mp_encoder, headers={'Content-Type': mp_encoder.content_type})
    assert response.status_code == 200


def test_me():
    response = client.get("/users/me", headers=get_auth_header())
    assert response.status_code == 200


def test_recipe_endpoints():
    DATA = {
        'name': 'testrecipe: 1',
        'description': 'test data',
        'oils': [
            {
                'name': 'olive',
                'ratio': .35
            },
            {
                'name': 'coconut',
                'ratio': .65
            }
        ],
        'weight': 800,
        'superfat': .05
    }
    # POST
    response = post(f"{BASE_URL}/recipes", headers=get_auth_header(), json=DATA)
    assert response.status_code == 201

    response_json = response.json()
    id = response_json['_id']

    # GET
    response = client.get(f"{BASE_URL}/recipes/{id}", headers=get_auth_header())
    assert response.status_code == 200

    # DELETE
    response = client.delete(f"/recipes/{id}", headers=get_auth_header(),)
    assert response.status_code == 204


def test_oils_endpoints():
    DATA = {
        'name': 'testoil',
        'sapratio': 0.123
    }
    # POST
    response = post(f"{BASE_URL}/oils", headers=get_auth_header(), json=DATA)
    assert response.status_code == 201
    
    response_json = response.json()
    id = response_json['_id']

    # GET
    response = client.get(f"{BASE_URL}/oils/{id}", headers=get_auth_header())
    assert response.status_code == 200

    # DELETE
    response = client.delete(f"/oils/{id}", headers=get_auth_header(),)
    assert response.status_code == 204


def test_user_endpoints():
    DATA = {
        'username': 'apitestuser',
        'full_name': 'api test',
        'email': 'apitest@example.com',
        'password1': 'Supersecret2!',
        'password2': 'Supersecret2!'
    }
    # POST
    response = post(f"{BASE_URL}/users", headers=get_auth_header(), json=DATA)
    assert response.status_code == 201
    
    response_json = response.json()
    id = response_json['_id']
    
    # DELETE
    response = client.delete(f"/users/{id}", headers=get_auth_header())
    assert response.status_code == 204

# need to add tests for
# 1. toggle admin
# 2. toggle disabled
# 3. update user
# 4. change user password 
# 5. failed status assertations
# 6. recipe calculations
# 7. unitest?