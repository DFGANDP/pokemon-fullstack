from sqlmodel import SQLModel, Field

class Pokemon(SQLModel, table=True):
    number: int = Field(primary_key=True)
    name: str
    generation: str
    height: int
    weight: int
    image: str

class PokemonType(SQLModel, table=True):
    pokemon_number: int = Field(foreign_key="pokemon.number", primary_key=True)
    pokemon_type: str = Field(primary_key=True)


class PokemonStat(SQLModel, table=True):
    pokemon_number: int = Field(foreign_key="pokemon.number", primary_key=True)
    name: str = Field(primary_key=True)
    value: int

class PokemonMove(SQLModel, table=True):
    pokemon_number: int = Field(foreign_key="pokemon.number", primary_key=True)
    pokemon_move: str = Field(primary_key=True)


class PokemonAbility(SQLModel, table=True):
    pokemon_number: int = Field(foreign_key="pokemon.number", primary_key=True)
    pokemon_ability: str = Field(primary_key=True)

class PokemonEvolution(SQLModel, table=True):
    from_name: str = Field(primary_key=True)
    to_name: str = Field(primary_key=True)
