from sqlalchemy import text
from backend.db import engine
with engine.begin() as conn:
    print(conn.execute(text("SELECT COUNT(*) FROM pokemon")).scalar())
    print(conn.execute(text("SELECT COUNT(*) FROM pokemontype")).scalar())
    print(conn.execute(text("SELECT COUNT(*) FROM pokemonevolution")).scalar())
