from typing import List
from sqlmodel import Session, select, col
from backend.db import engine
from backend.model.sql_model import Pokemon
from backend.model.schema import PokemonTable, PokemonQueryParams

class PokemonFilterBuilder:
    def build(self, query: PokemonQueryParams) -> List:
        filters = []

        if query.number: 
            filters.append(Pokemon.number == query.number)

        if query.name:
            filters.append(Pokemon.name.ilike(f"%{query.name}%"))

        if query.move:
            filters.append(Pokemon.name.ilike(f"%{query.move}%"))

        if query.type:
            filters.append(Pokemon.type == query.type) # single select for now 

        if query.generation:
            filters.append(Pokemon.generation == query.generation) # single select for now 

        return filters

# https://chatgpt.com/c/688fcdd6-e8fc-8325-ae67-8701866f6681

class PokemonService:
    def __init__(self, engine, query_builder: PokemonFilterBuilder):
        self.engine = engine
        self.query_builder = query_builder

    def get_pokemon_table(self, query: PokemonQueryParams) -> List[PokemonTable]:
        '''
        query.limit
        query.offset
        query.number
        query.name
        query.move
        query.type
        query.generation
        '''
        stmt = select(Pokemon) # Creates empty sql command

        filters = self.query_builder.build(query)
        for condition in filters:
            stmt = stmt.where(condition)

        # Add offset and limit 
        stmt = stmt.limit(query.limit).offset(query.offset)

        with Session(self.engine) as session:
            results = session.exec(stmt).all()
            return [PokemonTable.model_validate(p) for p in results]
