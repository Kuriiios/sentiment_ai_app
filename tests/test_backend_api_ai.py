#tests/test_backend_api_ai.py
from API_IA.sentiment_api import *

def test_analyse_sentiment():
    quote = {"text": "congrats"}
    dict = {"neg": 0.0, "neu": 0.0, "pos": 1.0, "compound": 0.5267 }
    print(quote['text'])
    citation = analyse_sentiment(quote)
    assert  citation == dict