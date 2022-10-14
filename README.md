# Soap Recipe API 

REST API built using FastAPI and MongoDB Atlas. The goal is to implement
authentication with Oauth2, full CRUD functionality and a dockerfile image.
This will be used in a future GCP or AWS infrastructure project 

## Setup

1. Clone repository
```
git clone https://github.com/blastomussa/soap-recipe-api.git
```
2. Install requirements
```
cd soap-recipe-api
pip install -r requirements.txt
```
3. Create a secret key for the hashing algorithm
```
cd app
openssl rand -hex 32 > .env
```
4. Open the .env file and add the following information
```
vim .env
```
```
SECRET_KEY = "***********" # result of openssl rand -hex 32 command
ACCESS_TOKEN_EXPIRE_MINUTES = 30
LOCAL_CONNECTION_STRING = "mongodb://127.0.0.1:27017" #for development on local instance of MongoDB
ATLAS_CONNECTION_STRING = "mongodb+srv://*******.mongodb.net/?retryWrites=true&w=majority" #from MongoDB Atlas Console
```
5. If running MongoDB on local machine modify connectionString.py to connect to your local instance declared in the .env file
```
CONNECTION_STRING = settings.atlas_connection_string 
# Uncomment to connect to local MongoDB instance 
#CONNECTION_STRING = settings.local_connection_string
```
4. Run application using uvicron
```
cd app
uvicorn main:app --reload --port 80 --host 0.0.0.0
```