from fastapi import APIRouter, HTTPException
from backend.service.pokemon_details_service import PokemonDetailsService
from backend.model.schema import PokemonDetail

router = APIRouter()

@router.get("/{name}", response_model=PokemonDetail)
def get_pokemon_by_name(name: str):
    '''Get details for given pokemon name'''
    try:
        name = name.lower()
        service = PokemonDetailsService()
        return service.get_pokemon_detail(name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))