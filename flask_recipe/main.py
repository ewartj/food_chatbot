from flask import Flask, render_template, request, redirect, url_for
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from form import RecipeForm
from initial_test import Recipes, check_if_ingredient
from constants import const
import pandas as pd
import os
import requests
from foodbert.food_extractor.food_model import FoodModel
from constants import const
model = FoodModel("chambliss/distilbert-for-food-extraction")

bot = ChatBot('Friend') #create the bot

trainer = ListTrainer(bot)

#bot.train(conv) # teacher train the bot

for knowledeg in os.listdir('base'):
	BotMemory = open('base/'+ knowledeg, 'r').readlines()
	trainer.train([
'Hi. Do you need help to find a recipe?',
'Yes',
'Okay what do you have?',
'No',
'Would you like a chat',
"Yes"
])

appid = const["appid"]
api_key = const["api_key"]


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/process',methods=['POST'])
def process():
	user_input=request.form['user_input']
	print(user_input)
	if user_input == "yes":
		print("Hiiiii")
		return redirect('/recipe')

	bot_response=bot.get_response(user_input)
	bot_response=str(bot_response)
	print("Friend: "+bot_response)
	return render_template('index.html',user_input=user_input,
		bot_response=bot_response
		)


@app.route("/recipe", methods=['GET', 'POST'])
def recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        data = str(form.query.data)
        print(data)
        # is_food = check_if_ingredient(data)
        # if is_food:
        seps = (',', ';', ' ', '|')
        # food = split(data, seps)
        ingrediants = model.extract_foods(data)
        ingredients_identified = get_ingredients(ingrediants)
        data = query_food_api(ingredients_identified, appid, api_key)
        output_data = pd.json_normalize(data["hits"], max_level=2)
        # print(output_data)
        return redirect(url_for('result', output_data=output_data))
    return render_template('recipe.html', form=form)

@app.route("/result", methods=['GET', 'POST'])
def result():
    result = request.args.get("output_data", None)
    return render_template("result.html", result=result)

def get_ingredients(food):
    ingredients = []
    for i in food:
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


def split(txt, seps):
    # https://stackoverflow.com/questions/4697006/python-split-string-by-list-of-separators
    default_sep = seps[0]

    # we skip seps[0] because that's the default separator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]


if __name__=='__main__':
	app.run()