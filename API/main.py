# API/main.py
from fastapi import FastAPI, HTTPException
import uvicorn
from loguru import logger 
import pandas as pd
from dotenv import load_dotenv 
from pydantic import BaseModel, Field
import os 
from API.modules.db_tools import read_db, read_id_db, initialize_db, add_row_db
from typing import List
import random 

load_dotenv()

class QuoteRequest(BaseModel):
    text : str = Field(min_length=1, default='your quote')

class QuoteResponse(BaseModel):
    id : int
    text : str    

class QuoteResponseId(BaseModel):
    id : int

app = FastAPI(title="API")

@app.get("/")
def read_root():
    return {"Hello": "World", "status": "API is running"}

@app.post("/insert/", response_model= QuoteResponse)
def insert_quote(quote : QuoteRequest):
    """Insère une nouvelle citation"""
    try:
        new_row =  add_row_db(quote.text)
        return new_row
    except Exception as e:
        logger.error(f"Insertion failed with error: {e}")
        raise HTTPException(
            status_code=400,
            detail="The server cannot or will not process the request due to an apparent client error "
        )

@app.get("/read/", response_model=List[QuoteResponse])
def read_all_quotes():
    try:
        df = pd.DataFrame(read_db())
        return df.reset_index().rename(columns={'id':'id','text':'text'}).to_dict('records')
    except Exception as e:
        logger.error(f"Reading db failed with error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected condition was encountered"
        )

@app.get("/read_ids/", response_model=List[QuoteResponseId])
def read_all_quotes_id():
    try:
        df = pd.DataFrame(read_id_db())
        return df.reset_index().rename(columns={'id':'id'}).to_dict('records')
    except Exception as e:
        logger.error(f"Reading ids failed with error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected condition was encountered"
        )

@app.get("/read/{id}", response_model=QuoteResponse)
def read_quote(id:int):
    try:
        df = pd.DataFrame(read_db())
        loc = id - 1
        if loc not in df.index:
            raise HTTPException (status_code=404, detail=f'Quote with ID {id} not found')
        quote_data = df.loc[loc].to_dict()
        quote_data['id'] = id

        return quote_data
    except Exception as e:
        logger.error(f"Reading specific id failed with error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected condition was encountered"
        )

@app.get("/read/random/", response_model=QuoteResponse)
def read_random_quotes():
    try:
        df = pd.DataFrame(read_db())

        if df.empty:
            raise HTTPException (status_code=404, detail=f'Dataframe {df} not found')
        random_id = random.choice(df.index)
        quote_data = df.loc[random_id].to_dict()
        quote_data['id'] = random_id

        return quote_data
    except Exception as e:
        logger.error(f"Reading specific id failed with error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected condition was encountered"
        )
     
if __name__ == "__main__":
    initialize_db()
    try:
        port = os.getenv('FAST_API_PORT', '8000')
        port = int(port)
        url = os.getenv('API_BASE_URL', '127.0.0.1')
    except ValueError:
        print("ERREUR")
        port = 8080

    uvicorn.run(
        "API.main:app",
        reload = False,
        port = port,
        host = url,
        log_level="debug"
    )