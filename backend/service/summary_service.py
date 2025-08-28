from sqlalchemy import func
from sqlmodel import Session, select

from backend.db import engine
from backend.model.sql_model import Pokemon, PokemonType


class SummaryService:
    def __init__(self):
        self.engine = engine

    def get_summary(self) -> dict:
        with Session(self.engine) as session:
            total_count = session.exec(select(func.count()).select_from(Pokemon)).one()

            type_counts = session.exec(
                select(PokemonType.pokemon_type, func.count()).group_by(PokemonType.pokemon_type)
            ).all()

            generation_counts = session.exec(
                select(Pokemon.generation, func.count()).group_by(Pokemon.generation)
            ).all()

        return {
            "total_pokemon": total_count,
            "count_by_type": dict(type_counts),
            "count_by_generation": dict(generation_counts),
        }
