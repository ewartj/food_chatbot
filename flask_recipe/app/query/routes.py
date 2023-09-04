from app.query import bp

from flask import Flask, render_template, request, redirect, url_for
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from initial_test import Recipes, check_if_ingredient
from constants import const
import pandas as pd
import os
import requests
from foodbert.food_extractor.food_model import FoodModel
from constants import const
from app.query.form import RecipeForm
from app.functions import (get_ingredients, query_food_api)
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

@bp.route("/recipe", methods=['GET', 'POST'])
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
            return redirect(url_for('query.result'))
        except:
             return redirect(url_for('query.none'))
    return render_template('recipe.html', form=form)

@bp.route("/result", methods=['GET', 'POST'])
def result():
    return render_template("result.html", result=result)

@bp.route("/none", methods=['GET', 'POST'])
def none():
    return render_template("none.html")

@bp.route("/result_db", methods=['GET', 'POST'])
def result_db():
    output_data = pd.read_csv("db.csv")
    output_json = output_data.to_json(orient='table',index=False)
    return output_json

@bp.route('/chat')
def chat():
	return render_template('chat.html')

@bp.route('/chat_process',methods=['POST'])
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