
import json
from pathlib import Path
from typing import Any, cast

from sqlmodel import Session

from backend.db import engine
from backend.model.sql_model import (
    Pokemon,
    PokemonAbility,
    PokemonEvolution,
    PokemonMove,
    PokemonStat,
    PokemonType,
)


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def load_data():
    data = load_json(Path("pokemon.json"))

    with Session(engine) as session:
        seen_abilities: set[tuple[int, str]] = set()
        seen_types: set[tuple[int, str]] = set()
        seen_moves: set[tuple[int, str]] = set()
        seen_stats: set[tuple[int, str]] = set()


        for p in data:
            name = p["name"].lower()

            session.add(
                Pokemon(
                    number=p["number"],
                    name=name,
                    generation=p["generation"],
                    height=p["height"],
                    weight=p["weight"],
                    image=p["image"],
                )
            )

            for t in p.get("types", []):
                t_lower = t.lower()
                key = (p["number"], t_lower)
                if key not in seen_types:
                    session.add(PokemonType(pokemon_number=p["number"], pokemon_type=t_lower))
                    seen_types.add(key)

            for stat in p.get("stats", []):
                stat_name = stat["name"].lower()
                key = (p["number"], stat_name)
                if key not in seen_stats:
                    session.add(
                        PokemonStat(pokemon_number=p["number"], name=stat_name, value=stat["value"])
                    )
                    seen_stats.add(key)

            for move in p.get("moves", []):
                move_lower = move.lower()
                key = (p["number"], move_lower)
                if key not in seen_moves:
                    session.add(PokemonMove(pokemon_number=p["number"], pokemon_move=move_lower))
                    seen_moves.add(key)

            for ability in p.get("abilities", []):
                ability_lower = ability.lower()
                key = (p["number"], ability_lower)
                if key not in seen_abilities:
                    session.add(
                        PokemonAbility(pokemon_number=p["number"], pokemon_ability=ability_lower)
                    )
                    seen_abilities.add(key)

            evo: dict[str, Any] = p.get("evolution", {})
            to_values = cast(list[str], evo.get("to") or [])

            # WŁAŚCIWE: dla KAŻDEGO to_name dodaj krawędź: current_name -> to_name
            for to_name in to_values:
                session.add(
                    PokemonEvolution(from_name=name, to_name=to_name.lower())
                )

        session.commit()


if __name__ == "__main__":
    load_data()
