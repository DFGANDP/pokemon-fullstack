from sqlmodel import SQLModel
from backend.db import engine
from backend.model.sql_model import Pokemon, PokemonType, PokemonStat, PokemonMove, PokemonAbility, PokemonEvolution

def init_db():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
