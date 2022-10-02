from os import getenv

if(getenv('DOCKER_IMG')):
    CONNECTION_STRING = "mongodb://host.docker.internal:27017"  # for local testing inside of docker
else:
    CONNECTION_STRING = "mongodb://127.0.0.1:27017" # for local testing in python outside of docker 
