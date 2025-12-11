# API/modules/db_tools.py
from sqlalchemy.sql.expression import select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from API.data.base import Base
from API.data.models import Quote
from loguru import logger 
import os 

DB_FILE_PATH = os.path.join("API","data", "quotes_db.db")
ENGINE = create_engine(f"sqlite:///{DB_FILE_PATH}", echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

def get_db_session() -> Session:
    """Fournit une session de BDD."""
    return SessionLocal()

def read_db():
    with get_db_session() as session:
        content = session.execute(select(Quote)).scalars().all()
        quotes = [{'id': row.id,'text': row.text } for row in content]
        return quotes

def read_id_db(id):
    with get_db_session() as session:
        content = session.execute(select(Quote).filter_by(id = id)).scalars().first()
        quotes = {'id': content.id,'text': content.text}
        return quotes

def read_ids_db():
    with get_db_session() as session:
        content = session.execute(select(Quote.id)).scalars().all()
        quotes = [{'id': row} for row in content]
        return quotes

def add_row_db(quote):
    with get_db_session() as session:
        print(f'THIS IS A QUOTE {quote}')
        new_quote = Quote(text=quote)
        session.add(new_quote)
        session.commit()
        injected_quote = session.query(Quote).filter_by(text=quote).first()
        session.close()
        return {'id' : injected_quote.id, 'text' : injected_quote.text}

def initialize_db():
    if os.path.exists(DB_FILE_PATH):
        logger.info("La base de données existe")
    else:
        logger.info(f"impossible de trouver le fichier {DB_FILE_PATH}")
        Base.metadata.create_all(ENGINE)
        sessionmaker(bind=ENGINE)
        logger.info(f"le fichier {DB_FILE_PATH} a été créé")