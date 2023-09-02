from app import app

from flask import Flask, render_template, request, redirect, url_for
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from app.form import RecipeForm
from initial_test import Recipes, check_if_ingredient
from constants import const
import pandas as pd
import os
import requests
from foodbert.food_extractor.food_model import FoodModel
from constants import const
from app.form import RecipeForm
from app.functions import (get_ingredients, get_recipe_info, 
                            query_food_api, split)
model = FoodModel("chambliss/distilbert-for-food-extraction")

appid = const["appid"]
api_key = const["api_key"]

bot = ChatBot('Friend')

trainer = ListTrainer(bot)
trainer.train([
'Hi. Do you need help to find a recipe?',
'Yes',
'Okay what do you have?',
'No',
'Would you like a chat',
"Yes"
])

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/process',methods=['POST'])
def process():
    old_responce = ""
    if os.path.exists("Output.txt"):
        with open('Output.txt', 'r') as file:
            old_responce = file.read().rstrip()
    user_input=request.form['user_input']
    print(user_input)
    if user_input == "yes" and old_responce == "Hi. Do you need help to find a recipe?":
        return redirect('/recipe')
    if user_input == "yes" and old_responce == "Would you like a chat":
        return redirect('/chat')

    bot_response=bot.get_response(user_input)
    bot_response=str(bot_response)
    with open("Output.txt", "w") as text_file:
        text_file.write(bot_response)
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
        df = pd.json_normalize(data["hits"], max_level=2)
        try:
            output_data = df[["recipe.label","recipe.source","recipe.url","recipe.cautions",
            "recipe.ingredientLines","recipe.cuisineType",
            "recipe.mealType","recipe.dishType"]]
            output_data.rename(columns=lambda x: x.replace("recipe.",""), inplace=True)
            output_data.reset_index(inplace=True)
            output_data.to_csv("db.csv")
            return redirect(url_for('result'))
        except:
             return redirect(url_for('none'))
    return render_template('recipe.html', form=form)

@app.route("/result", methods=['GET', 'POST'])
def result():
    return render_template("result.html", result=result)

@app.route("/none", methods=['GET', 'POST'])
def none():
    return render_template("none.html")

@app.route("/result_db", methods=['GET', 'POST'])
def result_db():
    output_data = pd.read_csv("db.csv")
    output_json = output_data.to_json(orient='table',index=False)
    return output_json

@app.route('/chat')
def chat():
	return render_template('chat.html')

@app.route('/chat_process',methods=['POST'])
def chat_process():
    user_input=request.form['user_input']
    r = requests.get(
        f'http://127.0.0.1:8000/chatbot/{user_input}'
        )
    data = r.json()
    bot_response=str(data)
    return render_template('chat.html',user_input=user_input,
		bot_response=bot_response
		)