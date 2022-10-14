from os import getenv
from config import settings

# Uncomment to connect to local or Atlas MongoDB instance 
CONNECTION_STRING = settings.atlas_connection_string  
#CONNECTION_STRING = settings.local_connection_string