# backend/main.py
from fastapi import FastAPI, HTTPException
import uvicorn
from loguru import logger 
import os 
import pandas as pd
from dotenv import load_dotenv 
from pydantic import BaseModel, StringConstraints, Field
from modules.db_tools import read_db, read_id_db, write_db, initialize_db, add_row_db
from typing import List
import requests
import random 
load_dotenv()

# modèles pydantic
class QuoteRequest(BaseModel):
    text : str = Field(min_length=1, default='your quote')

class QuoteResponse(BaseModel):
    id : int
    text : str    

class QuoteResponseId(BaseModel):
    id : int

# creation si besoin de la base de données
Session = initialize_db()

# --- Configuration ---
app = FastAPI(title="API")

PATH = "API/logs/main.log"
logger.remove()
logger.add(sink=PATH, rotation="500 MB", level="INFO")

@app.get("/")
def read_root():
    return {"Hello": "World", "status": "API is running"}

@app.post("/insert/", response_model= QuoteResponse)
def insert_quote(quote : QuoteRequest):
    """Insère une nouvelle citation"""
    try:
        session = Session()
        new_row =  add_row_db(session, quote.text)
        logger.info(f"Successfully inserted {new_row} into database")
        return new_row
    except requests.exceptions.RequestException as e:
        session.rollback()
        logger.error(f"Erreur de connexion à l'API : {e}")
    except Exception as e :
        logger.error(f"Une erreur est survenue: {e}")
        raise HTTPException(
            status_code=400,
            detail="The server cannot or will not process the request due to an apparent client error "
        )
    finally:
        session.close()


@app.get("/read/", response_model=List[QuoteResponse])
def read_all_quotes():
    try:
        session = Session()
        df = pd.DataFrame(read_db(session))
        logger.info('Read data from database')
        return df.reset_index().rename(columns={'id':'id','text':'text'}).to_dict('records')
    except requests.exceptions.RequestException as e:
        session.rollback()
        logger.error(f"Erreur de connexion à l'API : {e}")
    except Exception as e :
        logger.error(f"Une erreur est survenue: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected condition was encountered"
        )
    finally:
        session.close()

@app.get("/read_ids/", response_model=List[QuoteResponseId])
def read_all_quotes_id():
    try:
        session = Session()
        df = pd.DataFrame(read_id_db(session))
        logger.info('Read ids from database')
        return df.reset_index().rename(columns={'id':'id'}).to_dict('records')
    except requests.exceptions.RequestException as e:
        session.rollback()
        logger.error(f"Erreur de connexion à l'API : {e}")
    except Exception as e :
        logger.error(f"Une erreur est survenue: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected condition was encountered"
        )
    finally:
        session.close()

@app.get("/read/{id}", response_model=QuoteResponse)
def read_quote(id:int):
    try:
        session = Session()

        # get all quotes
        df = pd.DataFrame(read_db(session))
        # lower id by 1 to make it locator
        loc = id - 1
        # filter by id
        if loc not in df.index:
            raise HTTPException (status_code=404, detail=f'Quote with ID {id} not found')
        quote_data = df.loc[loc].to_dict()
        quote_data['id'] = id
        # return result
        logger.info(f'Read data from id:{id} from database')
        return quote_data
    except requests.exceptions.RequestException as e:
        session.rollback()
        logger.error(f"Erreur de connexion à l'API : {e}")
    except Exception as e :
        logger.error(f"Une erreur est survenue: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected condition was encountered"
        )
    finally:
        session.close()

@app.get("/read/random/", response_model=QuoteResponse)
def read_random_quotes():
    try:
        session = Session()
        df = pd.DataFrame(read_db(session))
        if df.empty:
            raise HTTPException (status_code=404, detail=f'Dataframe {df} not found')
        random_id = random.choice(df.index)
        quote_data = df.loc[random_id].to_dict()
        quote_data['id'] = random_id
        logger.info(f'Read data from id:{random_id} from database')
        return quote_data
    except requests.exceptions.RequestException as e:
        session.rollback()
        logger.error(f"Erreur de connexion à l'API : {e}")
    except Exception as e :
        logger.error(f"Une erreur est survenue: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected condition was encountered"
        )
    finally:
        session.close()

if __name__ == "__main__":
    try:
        print("Hello")
        port = os.getenv('FAST_API_PORT')
        url = os.getenv('API_BASE_URL')
        port = int(port)
        print(port)
    except ValueError:
        print("ERREUR")
        port = 8080

    uvicorn.run(
        "main:app", 
        host = url,
        port = port, 
        reload = True
    )