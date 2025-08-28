from fastapi import APIRouter, HTTPException, Depends

from typing import Annotated
from backend.db import engine
from backend.model.schema import PokemonQueryParams
from backend.service.pokemon_service import PokemonFilterBuilder, PokemonService

router = APIRouter()


@router.get("/")
def pokemon_table(
    query: Annotated[PokemonQueryParams, Depends()]
):
    try:
        query_builder = PokemonFilterBuilder()
        service = PokemonService(engine, query_builder)
        return service.get_pokemon_table(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
