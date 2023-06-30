from foodbert.food_extractor.food_model import FoodModel
from constants import const
import requests
import json
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
ingredients = []

for i in food:
    ingredient_tag = len(i['Ingredient'])
    if ingredient_tag > 0:
        print(ingredient_tag)
        for j, k in enumerate(i['Ingredient']):
            ingredients.append(i['Ingredient'][j]["text"])

# print(ingredients)

query = str(ingredients)

appid = const["appid"]
api_key = const["api_key"]

url = 'https://api.edamam.com/search?q=' + query + '&app_id=' + \
              appid + '&app_key=' + \
              api_key

r = requests.get(url)
data = r.json()

with open('data.json', 'w') as f:
    json.dump(data, f)


with open("data.json", "r") as read_file:
    data = json.load(read_file)

print(data.keys())
print(data["count"])
print(data["hits"][0]['recipe'].keys())
print(data["hits"][0]['recipe']["label"])
print(data["hits"][0]['recipe']["source"])
print(data["hits"][0]['recipe']["url"])
print(data["hits"][0]['recipe']["cautions"])

