from foodbert.food_extractor.food_model import FoodModel
from constants import const
import requests
import json
import re
model = FoodModel("chambliss/distilbert-for-food-extraction")

# examples = """3 tablespoons (21 grams) blanched almond flour
# ¾ teaspoon pumpkin spice blend
# ⅛ teaspoon baking soda
# ⅛ teaspoon Diamond Crystal kosher salt
# 1½ tablespoons maple syrup or 1 tablespoon honey
# 1 tablespoon (15 grams) canned pumpkin puree
# 1 teaspoon avocado oil or melted coconut oil
# ⅛ teaspoon vanilla extract
# 1 large egg""".split("\n")

examples = """Ingredients
1 large onion
1 red pepper
2 garlic cloves
1 tbsp oil
1 heaped tsp hot chilli powder (or 1 level tbsp if you only have mild)
1 tsp paprika
1 tsp ground cumin
500g lean minced beef
1 beef stock cube
400g can chopped tomatoes
½ tsp dried marjoram
1 tsp sugar (or add a thumbnail-sized piece of dark chocolate along with the beans instead, see tip)
2 tbsp tomato purée
410g can red kidney beans
plain boiled long grain rice, to serve
soured cream, to serve
""".split("\n")
examples = [x for x in examples if x]
# print(examples)

food = model.extract_foods(examples)

# print(food)

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


def query_food_api(query):
    query = str(query)
    appid = const["appid"]
    api_key = const["api_key"]
    url = 'https://api.edamam.com/search?q=' + query + '&app_id=' + \
                appid + '&app_key=' + \
                api_key
    r = requests.get(url)
    data = r.json()
    return data


# with open('data.json', 'w') as f:
#         json.dump(data, f)
# with open("data.json", "r") as read_file:
#     data = json.load(read_file)


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
     
    
# print(data.keys())
# print(data["count"])
# print(data["hits"][0]['recipe'].keys())
# print(data["hits"][0]['recipe']["label"])
# print(data["hits"][0]['recipe']["source"])
# print(data["hits"][0]['recipe']["url"])
# print(data["hits"][0]['recipe']["cautions"])

seps = (',', ';', ' ', '|')

user_ingredients = input("Please provide ingredients:")
food = split(user_ingredients, seps)
print(food)
ingrediants = model.extract_foods(food)
print(ingrediants)
ingredients_identified  = get_ingredients(ingrediants)
print(ingredients_identified)
data = query_food_api(ingredients_identified)
# with open('data.json', 'w') as f:
#         json.dump(data, f)
# with open("data.json", "r") as read_file:
#     data = json.load(read_file)
output_data = get_recipe_info(data)
print(output_data)




# query = str(ingredients)
