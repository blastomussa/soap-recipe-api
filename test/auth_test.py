from requests import post, get
from requests.exceptions import ConnectionError
from requests_toolbelt.multipart.encoder import MultipartEncoder #module used to encode form data


baseURL = "http://127.0.0.1"

def getToken(username,password):
        tokenURL  = f"{baseURL}/token"
        mp_encoder = MultipartEncoder(
            fields={
                'username': username,
                'password': password
            }
        )
        try:
            # {'Content-Type': mp_encoder.content_type} is important
            # sets the necessary boundy parameter in the content type header
            response = post(tokenURL, data=mp_encoder, headers={'Content-Type': mp_encoder.content_type})
            return(response.json())
        except ConnectionError:
            print("Connection Error. Please check your connection to the internet/server.")
            exit(1)


def authed_get(token, path, params=None):
        header = {
            'Authorization': f"Bearer {token}",
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            }
        try:
            response = get(url=path, headers=header, params=params)
            print(response)
            print(response.json())
        except ConnectionError:
            print("Connection Error. Please check your connection to the internet/server.")
            exit(1)


def getMe(access_token):
    path = f"{baseURL}/users/me"
    authed_get(access_token,path)


if __name__ == "__main__":
    token_json = getToken('johndoe', 'secret')
    getMe(token_json['access_token'])