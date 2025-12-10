''' 
@app.post('/analyse_sentiment/')
def analyse_sentiment(text:TextSentiment):
    try:
        sentiment = check_sentiment(text)
        logger.info(f"Résultats: {sentiment}")
        return sentiment
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")
        raise HTTPException(status_code=500, detail=str(e))
'''
from nltk.sentiment import SentimentIntensityAnalyzer

def check_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text.text)
    return sentiment