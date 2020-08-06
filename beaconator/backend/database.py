from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_engine(database_uri: str) -> Engine:
    engine = create_engine(database_uri, connect_args={"check_same_thread": False})
    return engine


def get_session(engine: Engine) -> sessionmaker:
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session


Base = declarative_base()
