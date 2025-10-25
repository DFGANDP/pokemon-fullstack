from fastapi import FastAPI

from backend.db import engine
from backend.model.sql_model import SQLModel
from backend.web.pokemon_details import router as details_router
from backend.web.pokemon_router import router as pokemon_router
from backend.web.summary_router import router as summary_router
from fastapi.middleware.cors import CORSMiddleware

# Create database tables
SQLModel.metadata.create_all(engine)

app = FastAPI(title="Pokemon API", description="Easy backend for pokemon review", version="1.0.0")

ALLOWED_ORIGINS = [
    "https://yellow-sea-060bba303.1.azurestaticapps.net",
    # ewentualnie lokalny dev:
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,      # NIE używaj "*" z allow_credentials=True
    allow_credentials=False,             # jeśli używasz cookies/autoryzacji z przeglądarki
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],                # lub lista: ["Authorization", "Content-Type", ...]
    expose_headers=[],
    max_age=600,
)


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
