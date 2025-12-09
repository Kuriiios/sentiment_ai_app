# API/sentiment_api.py
from fastapi import FastAPI
import uvicorn
from nltk.sentiment import SentimentIntensityAnalyzer
from pydantic import BaseModel
from loguru import logger
import nltk
import os 
from dotenv import load_dotenv 

load_dotenv()
nltk.download('vader_lexicon')

class TextSentiment (BaseModel):
    text: str

app = FastAPI(title='sentiment_app')

PATH = "API_IA/logs/sentiment_api.log"
logger.remove()
logger.add(sink=PATH)

@app.get("/")
def read_root():
    return {"Hello": "World", "status": "API AI is running"}

@app.post('/analyse_sentiment/')
def analyse_sentiment(text:TextSentiment):
    try:
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(text.text)
        logger.success(f'Analyze done on :{text.text}')
        return sentiment
    except Exception as e:
        logger.error(f'Analyze failed on :{text.text} due to errror {e}')


#SETUP UVICORN
if __name__ == "__main__":
    # 1 - on récupère le port de l'API
    try:
        print("Hello")
        port = os.getenv('FAST_API_AI_PORT')
        url = os.getenv('API_AI_BASE_URL')
        port = int(port)
        print(port)
    except ValueError:
        print("ERREUR")
        port = 8080

    # 2 - On lance uvicorn
    uvicorn.run(
        "sentiment_api:app", 
        host = url,
        port = port, 
        reload = False
    )