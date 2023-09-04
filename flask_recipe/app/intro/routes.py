from app.intro import bp

from flask import Flask, render_template, request, redirect, url_for
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from constants import const
import pandas as pd
import os
from foodbert.food_extractor.food_model import FoodModel
from constants import const
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

@bp.route('/')
@bp.route('/index')
def index():
	return render_template('index.html')

@bp.route('/process',methods=['POST'])
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