from foodbert.food_extractor.food_model import FoodModel
from constants import const
import requests
import json
import re
model = FoodModel("chambliss/distilbert-for-food-extraction")

#https://codereview.stackexchange.com/questions/280040/asking-multiple-choice-questions-in-python-using-an-api

def check_if_ingredient(query):
    print(f"query: {query}")
    pred = model.extract_foods(query)
    if len(pred) > 0:
        return True

class Recipes:
    def __init__(self, appid, api_key):
        self.appid = appid
        self.api_key = api_key

    def set_recipe_query(self, query):
        food = self._split(query)
        print(food)
        ingrediants = self._tokenise(food)
        print(ingrediants)
        self.query  = self._get_ingredients(ingrediants)


    def get_recipe_query(self):
        found_recipes = self._query_food_api()
        return found_recipes

    def _split(self, txt):
        # https://stackoverflow.com/questions/4697006/python-split-string-by-list-of-separators
        seps = (',', ';', ' ', '|')
        default_sep = seps[0]

        # we skip seps[0] because that's the default separator
        for sep in seps[1:]:
            txt = txt.replace(sep, default_sep)
        return [i.strip() for i in txt.split(default_sep)]
    
    def _tokenise(self, food):
        ingredients = model.extract_foods(food)
        return ingredients


    def _get_ingredients(self, ingrediants):
        ingredients_list = []
        for i in ingrediants:
            ingredient_tag = len(i['Ingredient'])
            if ingredient_tag > 0:
                print(ingredient_tag)
                for j, k in enumerate(i['Ingredient']):
                    ingredients_list.append(i['Ingredient'][j]["text"])
        return ingredients_list

    def _query_food_api(self):
        query = str(self.query)
        r = requests.get(
            'https://api.edamam.com/api/recipes/v2',
            headers={'Accept': 'application/json'},
            params={
                'app_id': self.appid,
                'app_key': self.api_key,
                'type': 'any',
                'q': query
            })
        data = r.json()
        return data


    def _get_recipe_info(data):
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

class Chatbot:
    def __init__(self, appid, api_key, model):
        self.recipie_query = Recipes(appid, api_key)
        self.model = model

    def chatbot_basic_greeting(self):
        greeting = input("Hello")
        if greeting.lower() == "Goodbye":
            print("Goodbye")
        need_recipe = input("Do you want to look for recipes?")
        if need_recipe.lower() == "No":
            print("Goodbye")
        self.cuisine = input("What cuisine do you like?")
        self.food_string = input("What do you have in your fridge?")
        count = 0
        while not self._check_if_ingredient(self.food_string):
            self.food_string = input("Could not identify any ingredients please try again")
            count += 1
            if count > 10:
                print("Could not identify ingredients please try later")
                break

    def _check_if_ingredient(query):
        print(f"query: {query}")
        ing = model.extract_foods(query)
        print(ing)
        if len(ing[['Ingredient']]) > 0:
            return True

    def find_recipes(self):
        self.recipie_query.set_recipe_query(str(self.food_string))
        self.output = self.recipie_query.get_recipe_query()
    
    def return_results(self):
        print(self.output)

# seps = (',', ';', ' ', '|')

# user_ingredients = input("Please provide ingredients:")
# food = split(user_ingredients, seps)
# print(food)
# ingrediants = model.extract_foods(food)
# print(ingrediants)
# ingredients_identified  = get_ingredients(ingrediants)
# print(ingredients_identified)
# appid = const["appid"]
# api_key = const["api_key"]
# data = query_food_api(ingredients_identified, appid, api_key)
# # with open('data.json', 'w') as f:
# #         json.dump(data, f)
# # with open("data.json", "r") as read_file:
# #     data = json.load(read_file)
# output_data = get_recipe_info(data)
# print(output_data)
