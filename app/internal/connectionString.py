from os import getenv
from config import settings

if(getenv('DOCKER_IMG')):
    CONNECTION_STRING = settings.atlas_connection_string  # for local testing inside of docker
else:
    CONNECTION_STRING = settings.local_connection_string # for local testing in python outside of docker 
