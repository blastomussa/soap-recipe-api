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
    i = 0
    for r in Recipe['oils']:
        name = r['name']
        w = r['ratio'] * weight #need to validate ratios; must total 1
        Recipe['oils'][i]['weight'] = w
        
        # calculate lye weight
        oil = client.api.oils.find_one({'name': name}) #need to validate if oil is found 
        converted_weight = w - (w * superfat)
        lye = converted_weight * oil['sapratio'] 
        Recipe['lye'] = Recipe['lye'] + lye
        i = i + 1
     
    return Recipe
