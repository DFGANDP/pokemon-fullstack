from sqlmodel import create_engine

DB_URL = "sqlite:///pokemon.db"
engine = create_engine(DB_URL, echo=True)
