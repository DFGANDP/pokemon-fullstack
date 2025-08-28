from typing import List
from sqlalchemy.engine import Engine
from sqlmodel import Session, select

from backend.model.schema import PokemonQueryParams, PokemonTable
from backend.model.sql_model import Pokemon


class PokemonFilterBuilder:
    def build(self, query: PokemonQueryParams) -> List:
        filters: List = []

        if query.number:
            filters.append(Pokemon.number == query.number)

        if query.name:
            filters.append(Pokemon.name.ilike(f"%{query.name}%"))

        if query.move:
            filters.append(Pokemon.name.ilike(f"%{query.move}%"))

        #if query.type_:
        #    filters.append(Pokemon.type == query.type_)  # single select for now

        #if query.generation:
        #    filters.append(Pokemon.generation == query.generation)  # single select for now

        return filters


# https://chatgpt.com/c/688fcdd6-e8fc-8325-ae67-8701866f6681


class PokemonService:
    def __init__(self, engine: Engine, query_builder: PokemonFilterBuilder):
        self.engine = engine
        self.query_builder = query_builder

    def get_pokemon_table(self, query: PokemonQueryParams) -> list[PokemonTable]:
        """
        query.limit
        query.offset
        query.number
        query.name
        query.move
        query.type
        query.generation
        """
        stmt = select(Pokemon)  # Creates empty sql command

        filters = self.query_builder.build(query)
        for condition in filters:
            stmt = stmt.where(condition)

        # Add offset and limit
        stmt = stmt.limit(query.limit).offset(query.offset)

        with Session(self.engine) as session:
            results = session.exec(stmt).all()
            print(results)
            return [PokemonTable.model_validate(p) for p in results]
