# API/sentiment_api.py
from fastapi import FastAPI, HTTPException
import uvicorn
from nltk.sentiment import SentimentIntensityAnalyzer
from pydantic import BaseModel
from loguru import logger
#from modules.db_tools import check_sentiment
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
logger.add(sink=PATH, rotation="500 MB", level="INFO")

@app.get("/")
def read_root():
    return {"Hello": "World", "status": "API AI is running"}

@app.post('/analyse_sentiment/')
def analyse_sentiment(text:TextSentiment):
    try:
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(text['text'])
        logger.info(f"Résultats: {sentiment}")
        return sentiment
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    try:
        port = os.getenv('FAST_API_AI_PORT')
        url = os.getenv('API_AI_BASE_URL')
        port = int(port)
    except ValueError:
        print("ERREUR")
        port = 8080

    uvicorn.run(
        "sentiment_api:app", 
        host = url,
        port = port, 
        reload = False
    )