from app.chat import bp
from flask import render_template, request
import requests

@bp.route('/chat')
def chat():
	return render_template('chat.html')

@bp.route('/chat_process',methods=['POST'])
def chat_process():
    user_input=request.form['user_input']
    r = requests.get(
        f'http://api_large:8000/chatbot/{user_input}'
        )
    data = r.json()
    bot_response=str(data)
    return render_template('chat.html',user_input=user_input,
		bot_response=bot_response
		)