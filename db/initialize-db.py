import requests
import pymongo

URL = "http://127.0.0.1:8000/oils"
DB_NAME = "api"
CONNECTION_STRING = "mongodb://localhost:27017"

OILS = [
    {'aloe': 0.171}, 
    {'apricotkernel': 0.135}, 
    {'avocado': 0.134}, 
    {'babussa': 0.179}, 
    {'beeswax': 0.067}, 
    {'canola': 0.123}, 
    {'castor': 0.129}, 
    {'cocoa': 0.138}, 
    {'coconut': 0.178}, 
    {'coffee': 0.134}, 
    {'corn': 0.135}, 
    {'cottonseed': 0.137}, 
    {'flaxseed': 0.136}, 
    {'grapeseed': 0.135}, 
    {'hazelnut': 0.136}, 
    {'hempseed': 0.138}, 
    {'jojoba': 0.066}, 
    {'lard': 0.138}, 
    {'mango': 0.135}, 
    {'mustard': 0.123}, 
    {'neem': 0.14}, 
    {'olive': 0.135}, 
    {'palm': 0.141}, 
    {'peanut': 0.135}, 
    {'pumpkinseed': 0.138}, 
    {'ricebran': 0.135}, 
    {'sesame': 0.137}, 
    {'shea': 0.128}, 
    {'soybean': 0.135}, 
    {'sunflower': 0.136}, 
    {'sweetalmond': 0.135}, 
    {'walnut': 0.138}
]

def createOilsDB():
    for oil in OILS:
        k = list(oil.keys())
        v = list(oil.values())
        name = str(k[0])
        sapratio = float(v[0])
        oil = {
            '_id': None, 
            'name': name, 
            'sapratio': sapratio
        }
        response = requests.post(URL,json=oil)
        print(response.json())


def deleteAllDocs(colName):
    client = pymongo.MongoClient(CONNECTION_STRING)
    validate(client)

    db = client[DB_NAME]
    col = db[colName]
    col.delete_many({})


def dropCol(colName):
    client = pymongo.MongoClient(CONNECTION_STRING)
    validate(client)
    db = client[DB_NAME]
    col = db[colName]
    col.drop()
    print(db.list_collection_names())


def getCols():
    client = pymongo.MongoClient(CONNECTION_STRING)
    validate(client)
    db = client[DB_NAME]
    print(db.list_collection_names())


def validate(client):
    try:
        client.server_info() # validate connection string
    except pymongo.errors.ServerSelectionTimeoutError:
        raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")



if __name__ == "__main__": 
    getCols()
    #delete()