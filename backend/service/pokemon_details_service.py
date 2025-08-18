from sqlmodel import Session, select
from backend.db import engine
from backend.model.sql_model import (
    Pokemon, PokemonType, PokemonMove, PokemonStat, 
    PokemonAbility, PokemonEvolution
)

class PokemonDetailsService:
    def __init__(self):
        self.engine = engine

    def get_pokemon_detail(self, name: str) -> dict:
        with Session(self.engine) as session:
            # Główne dane
            pokemon = session.exec(
                select(Pokemon).where(Pokemon.name == name)
            ).first()
            if not pokemon:
                raise ValueError("Pokemon not found")

            # Types
            types = session.exec(
                select(PokemonType.pokemon_type).where(
                    PokemonType.pokemon_number == pokemon.number
                )
            ).all()

            # Stats
            stats_raw = session.exec(
                select(PokemonStat.name, PokemonStat.value).where(
                    PokemonStat.pokemon_number == pokemon.number
                )
            ).all()
            stats = {name: value for name, value in stats_raw}

            # Moves
            moves = session.exec(
                select(PokemonMove.pokemon_move).where(
                    PokemonMove.pokemon_number == pokemon.number
                )
            ).all()

            # Abilities
            abilities = session.exec(
                select(PokemonAbility.pokemon_ability).where(
                    PokemonAbility.pokemon_number == pokemon.number
                )
            ).all()

            # Evolution
            from_result = session.exec(
                select(PokemonEvolution.from_name).where(
                    PokemonEvolution.to_name == pokemon.name
                )
            ).first()

            to_result = session.exec(
                select(PokemonEvolution.to_name).where(
                    PokemonEvolution.from_name == pokemon.name
                )
            ).all()

            evolution = {
                "from": from_result,
                "to": to_result
            }

        return {
            "number": pokemon.number,
            "name": pokemon.name,
            "generation": pokemon.generation,
            "height": pokemon.height,
            "weight": pokemon.weight,
            "types": types,
            "stats": stats,
            "moves": moves,
            "abilities": abilities,
            "evolution": evolution,
            "image": pokemon.image
        }
