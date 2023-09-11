from fastapi import FastAPI
import uvicorn
import os
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = FastAPI()

english_bot = ChatBot("Chatterbot")

trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("chatterbot.corpus.english")

@app.get("/chatbot/{query}")
async def input(query: str):
    return str(english_bot.get_response(query))

if __name__ == "__main__":
    uvicorn.run("main:app", port=int(os.getenv('APP_PORT')), host='0.0.0.0')