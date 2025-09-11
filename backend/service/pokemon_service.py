# service.py
from sqlalchemy import func, exists, select as sa_select
from sqlmodel import Session, select
from backend.model.sql_model import Pokemon, PokemonType, PokemonMove
from backend.model.schema import PokemonQueryParams, PokemonTable

class PokemonFilterBuilder:
    def build(self, query: PokemonQueryParams):
        filters = []

        if query.number is not None:
            filters.append(Pokemon.number == query.number)

        if query.name:
            filters.append(Pokemon.name.ilike(f"%{query.name}%"))

        if query.move:
            # filtr po ruchu -> EXISTS na PokemonMove
            subq_move = (
                sa_select(1)
                .select_from(PokemonMove)
                .where(
                    PokemonMove.pokemon_number == Pokemon.number,
                    PokemonMove.pokemon_move.ilike(f"%{query.move}%"),
                )
                .limit(1)
            )
            filters.append(exists(subq_move))

         #jeśli chcesz filtry po type_/generation:
        if query.type_:
            subq_type = (
                sa_select(1)
                .select_from(PokemonType)
                .where(
                    PokemonType.pokemon_number == Pokemon.number,
                    PokemonType.pokemon_type == query.type_,
                )
                .limit(1)
            )
            filters.append(exists(subq_type))

        if query.generation:
            filters.append(Pokemon.generation == query.generation)

        return filters


class PokemonService:
    def __init__(self, engine, query_builder: PokemonFilterBuilder):
        self.engine = engine
        self.query_builder = query_builder

    def get_pokemon_table(self, query: PokemonQueryParams) -> list[PokemonTable]:
        # --- Kolumny wyliczane (subquery skorelowane) ---
        type_one_sq = (
            sa_select(PokemonType.pokemon_type)
            .where(PokemonType.pokemon_number == Pokemon.number)
            .order_by(PokemonType.pokemon_type)   # deterministycznie: alfabetycznie
            .limit(1)
            .scalar_subquery()
        )
        type_two_sq = (
            sa_select(PokemonType.pokemon_type)
            .where(PokemonType.pokemon_number == Pokemon.number)
            .order_by(PokemonType.pokemon_type)
            .offset(1)  # drugi typ
            .limit(1)
            .scalar_subquery()
        )
        moves_count_sq = (
            sa_select(func.count())
            .select_from(PokemonMove)
            .where(PokemonMove.pokemon_number == Pokemon.number)
            .scalar_subquery()
        )

        type_one_col = type_one_sq.label("type_one")
        type_two_col = type_two_sq.label("type_two")
        moves_count_col = moves_count_sq.label("moves_count")

        # --- SELECT z projekcją (konkretne kolumny + aliasy) ---
        stmt = select(
            Pokemon.number,
            Pokemon.name,
            Pokemon.generation,
            Pokemon.height,
            Pokemon.weight,
            Pokemon.image,
            type_one_col,
            type_two_col,
            moves_count_col,
        )

        # --- Filtry ---
        for cond in self.query_builder.build(query):
            stmt = stmt.where(cond)

        # --- Sortowanie (uwzględnia także aliasy) ---
        SORT_MAP = {
            "number": Pokemon.number,
            "name": Pokemon.name,
            "generation": Pokemon.generation,
            "height": Pokemon.height,
            "weight": Pokemon.weight,
            "type_one": type_one_col,
            "type_two": type_two_col,
            "moves_count": moves_count_col,
        }
        sort_col = SORT_MAP.get(query.sort_by or "number", Pokemon.number)
        stmt = stmt.order_by(sort_col.asc() if query.sort_order == "asc" else sort_col.desc())

        # --- Paginacja ---
        stmt = stmt.limit(query.limit).offset(query.offset)

        # --- Wykonanie i mapowanie do Pydantic ---
        with Session(self.engine) as session:
            rows = session.exec(stmt).all()
            # rows to list[Row]; row._mapping -> dict-like: {"number":..., "type_one":...}
            return [PokemonTable.model_validate(dict(r._mapping)) for r in rows]
