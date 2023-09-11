from app.intro import bp

from flask import render_template, request, redirect
from constants import const
import os
from foodbert.food_extractor.food_model import FoodModel
from constants import const
import requests

model = FoodModel("chambliss/distilbert-for-food-extraction")

appid = const["appid"]
api_key = const["api_key"]

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

    r = requests.get(
        f'http://api_intro:5050/chatbot/{user_input}'
        )
    data = r.json()
    bot_response=str(data)

    if user_input == "yes" and old_responce == "Hi. Do you need help to find a recipe?":
        return redirect('/recipe')
    if user_input == "yes" and old_responce == "Would you like a chat":
        return redirect('/chat')

    # bot_response=bot.get_response(user_input)
    # bot_response=str(bot_response)
    with open("Output.txt", "w") as text_file:
        text_file.write(bot_response)
    return render_template('index.html',user_input=user_input,
		bot_response=bot_response
		)