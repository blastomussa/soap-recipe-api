# to be used with pytest
from fastapi.testclient import TestClient
from requests_toolbelt.multipart.encoder import MultipartEncoder
from requests import post
from pymongo import MongoClient

# required to find all packages in app for pytest; otherwise ModuleImport Error
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from .main import app
from internal.connectionString import CONNECTION_STRING


client = TestClient(app)

BASE_URL = "http://127.0.0.1"

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


def test_recipe():
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

    response = post(f"{BASE_URL}/recipes", headers=get_auth_header(), json=DATA)
    assert response.status_code == 201
    
    response_json = response.json()
    id = response_json['_id']

    response = client.delete(f"/recipes/{id}", headers=get_auth_header(),)
    assert response.status_code == 200


# NOT WORKING RIGHT, _ID  keyerror
def test_oils():
    DATA = {
        'name': 'testoil12',
        'sapratio': 0.123
    }

    response = post(f"{BASE_URL}/oils", headers=get_auth_header(), json=DATA)
    assert response.status_code == 201
    
    response_json = response.json()
    print(response_json)
    id = response_json['_id']

    response = client.delete(f"/oils/{id}", headers=get_auth_header(),)
    assert response.status_code == 200
