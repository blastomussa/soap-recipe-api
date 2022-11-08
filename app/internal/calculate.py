from pymongo import MongoClient
from internal.validateDBConnection import validateMongo
from internal.connectionString import CONNECTION_STRING


def calculateRecipe(Recipe):

    weight = Recipe['weight']
    superfat = Recipe['superfat']

    # 1:3 liquid to oil ratio
    liquid = weight * .33
    Recipe['liquid'] = liquid
    Recipe['lye'] = 0

    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)

    # calculate individual oil weights and update dictionary
    index = 0
    total_ratio = 0
    for r in Recipe['oils']:
        total_ratio = total_ratio + r['ratio']
        name = r['name']
        w = r['ratio'] * weight
        Recipe['oils'][index]['weight'] = w
        index = index + 1
        
        # calculate lye weight
        if client.api.oils.find_one({'name': name}): #validate if oil is found in DB
            oil = client.api.oils.find_one({'name': name})
            converted_weight = w - (w * superfat)
            l = converted_weight * oil['sapratio'] 
            lye = round(l,2)
            Recipe['lye'] = Recipe['lye'] + lye
        else:
            return f'{name} oil not found.'

    if total_ratio != 1.0:
            return "Ratio of oils must equal 1"   # total ratio must equal 1
     
    return Recipe
