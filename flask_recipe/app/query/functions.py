from constants import const
import requests
from constants import const

appid = const["appid"]
api_key = const["api_key"]

def get_ingredients(food):
    ingredients = []
    for i in food:
        ingredient_tag = len(i['Ingredient'])
        if ingredient_tag > 0:
            for j, k in enumerate(i['Ingredient']):
                ingredients.append(i['Ingredient'][j]["text"])
    return ingredients

def query_food_api(query, appid, api_key):
    query = str(query)
    r = requests.get(
        'https://api.edamam.com/api/recipes/v2',
        headers={'Accept': 'application/json'},
        params={
            'app_id': appid,
            'app_key': api_key,
            'type': 'any',
            'q': query
        })
    print(r)
    data = r.json()
    return data

def get_recipe_info(data):
    recipes_dict = {}
    total_matches = data["count"]
    for i in range(0, total_matches):
        recipes_dict[data["hits"][0]['recipe']["label"]] = {
            "source":data["hits"][0]['recipe']["source"],
            "url":data["hits"][0]['recipe']["url"],
            "cautions":data["hits"][0]['recipe']["cautions"]
        }
    return recipes_dict