from typing import Dict
from sqlmodel import Session, select
from backend.db import engine
from backend.model.sql_model import Pokemon, PokemonType
from sqlalchemy import func


class SummaryService:
    def __init__(self):
        self.engine = engine

    def get_summary(self) -> Dict:
        with Session(self.engine) as session:
            total_count = session.exec(
                select(func.count()).select_from(Pokemon)
            ).one()

            type_counts = session.exec(
                select(PokemonType.pokemon_type, func.count())
                .group_by(PokemonType.pokemon_type)
            ).all()

            generation_counts = session.exec(
                select(Pokemon.generation, func.count())
                .group_by(Pokemon.generation)
            ).all()

        return {
            "total_pokemon": total_count,
            "count_by_type": {t: c for t, c in type_counts},
            "count_by_generation": {g: c for g, c in generation_counts}
        }
