from sqlmodel import SQLModel
from backend.db import engine

# KLUCZOWE: import modułu z klasami modeli, żeby zarejestrowały tabele
from backend.model import sql_model as _models  # noqa: F401

def init_db():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
