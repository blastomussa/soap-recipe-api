import pymongo

CONNECTION_STRING = "mongodb://localhost:27017"

def calculate_recipe(Recipe):
    weight = Recipe['weight']
    superfat = Recipe['superfat']

    # 1:3 liquid to oil ratio
    liquid = weight * .33
    Recipe['liquid'] = liquid
    client = pymongo.MongoClient(CONNECTION_STRING)
    validateMongo(client)

    db = client['api']
    col = db['oils']

    # calculate individual oil weights and update dictionary
    i = 0
    for r in Recipe['oils']:
        name = r['name']
        w = r['ratio'] * weight #need to validate ratios; must total 1
        Recipe['oils'][i]['weight'] = w
        
        # calculate lye weight
        search = list(col.find({'name': name})) #need to validate if oil is found 
        converted_weight = w - (w * superfat)
        lye = converted_weight * search[0]['sapratio']
        if Recipe['lye']: 
            Recipe['lye'] = Recipe['lye'] + lye
        else:
            Recipe['lye'] = lye
        i = i + 1
 
    return Recipe


def validateMongo(client):
    try:
        client.server_info() # validate connection string
    except pymongo.errors.ServerSelectionTimeoutError:
        raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")