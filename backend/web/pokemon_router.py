from fastapi import APIRouter, HTTPException, Query, Depends
from backend.db import engine
from backend.service.pokemon_service import PokemonService, PokemonFilterBuilder
from backend.model.schema import PokemonQueryParams

router = APIRouter()

@router.get("/")
def pokemon_table(
    query: PokemonQueryParams = Depends(),
):
    try:
        query_builder = PokemonFilterBuilder()
        service = PokemonService(engine, query_builder)
        return service.get_pokemon_table(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))