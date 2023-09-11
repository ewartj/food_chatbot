from fastapi import FastAPI
import uvicorn
import os
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

app = FastAPI()

bot = ChatBot('Query')

trainer = ListTrainer(bot)
trainer.train([
'Hi. Do you need help to find a recipe?',
'Yes',
'Would you like a chat',
"Yes"
])

@app.get("/chatbot/{query}")
async def input(query: str):
    return str(bot.get_response(query))

if __name__ == "__main__":
    uvicorn.run("main:app", port=int(os.getenv('APP_PORT')), host='0.0.0.0')