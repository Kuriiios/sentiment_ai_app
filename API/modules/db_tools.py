# backend/modules/db_tools.py
from sqlalchemy.sql.expression import insert, delete, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from data.base import Base
from data.models import Quote
from loguru import logger 
import pandas as pd
import os 

DB_FILE_PATH = os.path.join("API","data", "quotes_db.db")

def write_db(engine):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session

def read_db(session):
    try:
        content = session.execute(select(Quote)).scalars().all()
        quotes = [{'id': row.id,'text': row.text } for row in content]
        logger.success(f"Successfully read from database")
        return quotes
    except Exception as e:
        logger.error(f"Failed to add row with error: {e}")
        session.rollback()
    finally:
        session.close()


def read_id_db(session):
    try:
        content = session.execute(select(Quote.id)).scalars().all()
        quotes = [{'id': row} for row in content]
        logger.success(f"Successfully read id from database")
        return quotes
    except Exception as e:
        logger.error(f"Failed to add row with error: {e}")
        session.rollback()
    finally:
        session.close()

def add_row_db(session, quote):
    try:
        new_quote = Quote(text=quote)
        session.add(new_quote)
        session.commit()
        injected_quote = session.query(Quote).filter_by(text=quote).first()
        quote_object  = {'id' : injected_quote.id, 'text' : injected_quote.text}
        logger.success(f"Successfully added data : {quote_object} to database")
        return quote_object
    except Exception as e:
        logger.error(f"Failed to add row with error: {e}")
        session.rollback()
    finally:
        session.close()

def initialize_db():
    engine = create_engine("sqlite:///API/data/quotes_db.db", echo=True)

    if os.path.exists(DB_FILE_PATH):
        logger.info("La base de données existe")
    else:
        logger.info(f"impossible de trouver le fichier {DB_FILE_PATH}")
        Session = write_db(engine)
        logger.info(f"le fichier {DB_FILE_PATH} a été créé")
        return Session
    Session = sessionmaker(bind=engine)
    return Session

  