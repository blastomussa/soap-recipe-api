# to be used with pytest
from fastapi.testclient import TestClient
from requests_toolbelt.multipart.encoder import MultipartEncoder
from requests import post

# required to find all packages in app for pytest; otherwise ModuleImport Error
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from .main import app

client = TestClient(app)

baseURL = "http://127.0.0.1"

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
                'username': 'joedoe',
                'password': 'Supersecret2!'
            }
    )
    response = post(f"{baseURL}/token",data=mp_encoder, headers={'Content-Type': mp_encoder.content_type})
    assert response.status_code == 200


def test_authed_get():
    mp_encoder = MultipartEncoder(
            fields={
                'username': 'joedoe',
                'password': 'Supersecret2!'
            }
    )
    response = post(f"{baseURL}/token",data=mp_encoder, headers={'Content-Type': mp_encoder.content_type})
    response_json = response.json()
    token = response_json['access_token']
    
    header = {
        'Authorization': f"Bearer {token}",
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        }
    response = client.get("/users/me", headers=header)
    assert response.status_code == 200
