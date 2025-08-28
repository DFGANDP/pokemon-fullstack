from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal

# Pokemon Summary


class TypeCount(BaseModel):
    pokemon_type: str
    count: int


class GenerationCount(BaseModel):
    generation: str
    count: int


class SummaryResponse(BaseModel):
    total_pokemon: int
    count_by_type: dict[str, int]
    count_by_generation: dict[str, int]


# Pokemon Table


class PokemonQueryParams(BaseModel):
    limit: int = Field(25, ge=1, le=100, description="Number of Pokemon to return")
    offset: int = Field(0, ge=0, description="Number of Pokemon to skip")

    number: Optional[int] = Field(None, description="Unique number of the Pokemon")
    name: Optional[str] = Field(None, description="Freetext search by name")
    move: Optional[str] = Field(None, description="Freetext search by move")

    # alias 'type' w URL: ?type=fire -> type_ w modelu
    type_: Optional[str] = Field(None, alias="type", description="Dropdown filter by type")
    generation: Optional[str] = Field(None, description="Dropdown filter by generation")

    sort_by: Optional[
        Literal["number", "name", "generation", "height", "weight", "type_one", "type_two", "moves_count"]
    ] = "number"
    sort_order: Optional[Literal["asc", "desc"]] = "asc" # ograniczna co mozna wpisac w to pole LITERAL 

    model_config = ConfigDict(populate_by_name=True)


class PokemonTable(BaseModel):
    number: int
    name: str
    generation: str
    height: int
    weight: int
    type_one: str
    type_two: Optional[str] = None
    moves_count: int
    model_config = {
        "from_attributes": True  # <-- nowa opcja dla ORM
    } # from_attributes=True pozwala brać dane także z atrybutów obiektu (obj.field).


# Pokemon Details


class PokemonDetail(BaseModel):
    number: int
    name: str
    generation: str
    height: int
    weight: int
    types: list[str]
    stats: dict[str, int]
    moves: list[str]
    abilities: list[str]
    evolution: dict[str, list[str] | None]
    image: str
