from fastapi import FastAPI

from backend.db import engine
from backend.model.sql_model import SQLModel
from backend.web.pokemon_details import router as details_router
from backend.web.pokemon_router import router as pokemon_router
from backend.web.summary_router import router as summary_router

# Create database tables
SQLModel.metadata.create_all(engine)

app = FastAPI(title="Pokemon API", description="Easy backend for pokemon review", version="1.0.0")

# Include routers with proper prefixes
app.include_router(summary_router, prefix="/api/v1/summary", tags=["summary"])
app.include_router(pokemon_router, prefix="/api/v1/pokemon", tags=["pokemon"])
app.include_router(details_router, prefix="/api/v1/details", tags=["details"])


@app.get("/")
def root():
    return {
        "message": "Welcome in Pokemon API!",
        "version": "1.0.0",
        "available_endpoints": {
            "summary": "/api/v1/summary",
            "pokemon": "/api/v1/pokemon",
            "details": "/api/v1/details",
            "docs": "/docs",
            "redoc": "/redoc",
        },
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
