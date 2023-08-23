from foodbert.food_extractor.food_model import FoodModel
from constants import const
import requests
import pandas as pd
import json
import re
model = FoodModel("chambliss/distilbert-for-food-extraction")


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
    for i in range(0, total_matches):
        recipes_dict[data["hits"][0]['recipe']["label"]] = {
            "source":data["hits"][0]['recipe']["source"],
            "url":data["hits"][0]['recipe']["url"],
            "cautions":data["hits"][0]['recipe']["cautions"]
        }
    return recipes_dict
     
seps = (',', ';', ' ', '|')

user_ingredients = input("Please provide ingredients:")
# food = split(user_ingredients, seps)
# print(food)
ingrediants = model.extract_foods(user_ingredients)
print(ingrediants)
ingredients_identified  = get_ingredients(ingrediants)
print(ingredients_identified)
appid = const["appid"]
api_key = const["api_key"]
data = query_food_api(ingredients_identified, appid, api_key)
# print(data)
# with open('data.json', 'w') as f:
#         json.dump(data, f)
# # with open("data.json", "r") as read_file:
# #     data = json.load(read_file)
# output_data = get_recipe_info(data)
# print(output_data)


# with open("data.json", "r") as read_file:
#     data = json.load(read_file)


# print(data.keys())
# print(data["count"])
# print(data["hits"][0]['recipe'].keys())
# print(data["hits"][0]['recipe']["label"])
# print(data["hits"][0]['recipe']["source"])
# print(data["hits"][0]['recipe']["url"])
# print(data["hits"][0]['recipe']["cautions"])

data2 = data["hits"]
df = pd.json_normalize(data2, max_level=2)
df.to_csv("test.csv")
print(df)

total_count = 10
# if data["count"] > 10:
#     total_count = 10
# for i in range(0,data["count"]):
#     print(data["hits"][i])#['recipe']["label"])

# query = ["peppers","rice","chicken"]
# query = str(query)
# appid = const["appid"]
# api_key = const["api_key"]
# url = 'https://api.edamam.com/search?q=' + query + '&app_id=' + \
#             appid + '&app_key=' + \
#             api_key


# url = "https://api.edamam.com/search" #"https://edamam-food-and-grocery-database.p.rapidapi.com/parser"
# headers = {"Content-Type": "application/json"}
# parameters = {
#     'q':query,
#     'app_id': const["appid"],
#     'app_key': const["api_key"]
#     }
# response = requests.get(
#         'https://api.edamam.com/api/recipes/v2',
#         headers={'Accept': 'application/json'},
#         params={
#             'app_id': const["appid"],
#             'app_key': const["api_key"],
#             'q': query
#             # 'type': 'any',
#             # 'mealType': meal_type,
#             # 'health': health_restriction,
            
#         }
# r = requests.get(
#         'https://api.edamam.com/api/recipes/v2',
#         headers={'Accept': 'application/json'},
#         params={
#             'app_id': const["appid"],
#             'app_key': const["api_key"],
#             'type': 'any',
#             'q': query
#         })
# data = r.json()
# with open('data2.json', 'w') as f:
#          json.dump(data, f)