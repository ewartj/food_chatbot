from foodbert.food_extractor.food_model import FoodModel
from constants import const
import requests
import json
import re
model = FoodModel("chambliss/distilbert-for-food-extraction")

#https://codereview.stackexchange.com/questions/280040/asking-multiple-choice-questions-in-python-using-an-api
def split(txt, seps):
    # https://stackoverflow.com/questions/4697006/python-split-string-by-list-of-separators
    default_sep = seps[0]

    # we skip seps[0] because that's the default separator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]


def get_ingredients(food):
    ingredients = []
    for i in food:
        print(i)
        ingredient_tag = len(i['Ingredient'])
        if ingredient_tag > 0:
            print(ingredient_tag)
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
    data = r.json()
    return data


def get_recipe_info(data):
    recipes_dict = {}
    total_matches = data["count"]
    if total_matches > 10:
        total_matches = 10
    print(total_matches)
    for i in range(0, total_matches):
        recipes_dict[data["hits"][i]['recipe']["label"]] = {
            "source":data["hits"][i]['recipe']["source"],
            "url":data["hits"][i]['recipe']["url"],
            "cautions":data["hits"][i]['recipe']["cautions"]
        }
    return recipes_dict
     
seps = (',', ';', ' ', '|')

user_ingredients = input("Please provide ingredients:")
food = split(user_ingredients, seps)
print(food)
ingrediants = model.extract_foods(food)
print(ingrediants)
ingredients_identified  = get_ingredients(ingrediants)
print(ingredients_identified)
appid = const["appid"]
api_key = const["api_key"]
data = query_food_api(ingredients_identified, appid, api_key)
# with open('data.json', 'w') as f:
#         json.dump(data, f)
# with open("data.json", "r") as read_file:
#     data = json.load(read_file)
output_data = get_recipe_info(data)
print(output_data)
