from pydantic import BaseModel, Field
from typing import Dict, List, Optional

# Pokemon Summary

class TypeCount(BaseModel):
    pokemon_type: str
    count: int


class GenerationCount(BaseModel):
    generation: str
    count: int


class SummaryResponse(BaseModel):
    total_pokemon: int
    count_by_type: Dict[str, int]
    count_by_generation: Dict[str, int]

# Pokemon Table

class PokemonQueryParams(BaseModel):
    limit: int = Field(25, ge=1, le=25, description="Number of Pokemon to return")
    offset: int = Field(0, ge=0, description="Number of Pokemon to skip")

    number: Optional[int] = Field(None, description="Unique number of the Pokemon")
    name: Optional[str] = Field(None, description="Freetext search by name")
    move: Optional[str] = Field(None, description="Freetext search by move")
    
    type: Optional[str] = Field(None, description="Dropdown filter by type")
    generation: Optional[str] = Field(None, description="Dropdown filter by generation")

class PokemonTable(BaseModel):
    number: int
    name: str
    generation: str
    height: int
    weight: int
    type_one: str
    type_two: Optional[str]
    moves_count: int
    model_config = {
        "from_attributes": True  # <-- nowa opcja dla ORM
    }
# Pokemon Details

class PokemonDetail(BaseModel):
    number: int
    name: str
    generation: str
    height: int
    weight: int
    types: List[str]
    stats: Dict[str, int]
    moves: List[str]
    abilities: List[str]
    evolution: Dict[str, Optional[List[str]]]
    image: str


