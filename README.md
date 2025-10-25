## What is it

A simple project for browsing Pokémon data: backend in Python (FastAPI + SQLModel + SQLite) and frontend in Vue 3 (Vite + TypeScript + PrimeVue). The backend provides an API with list, details, and summary endpoints, while the frontend displays the data in a clear form.

## Live Demo

The application is deployed on Azure Static Web Apps and can be accessed at:

**🌐 [https://yellow-sea-060bba303.1.azurestaticapps.net/](https://yellow-sea-060bba303.1.azurestaticapps.net/)**

## Overview

* Backend (`backend/`): FastAPI with three routers: `summary`, `pokemon`, and `details`. SQLite database, initialization and data loading from the `pokemon.json` source via scripts in `backend/scripts/`. Deployed on Azure with CORS configured for the frontend.
* Frontend (`frontend/`): Vue 3 + Vite application. Routing, components, and a simple API client in `src/api/`. Deployed on Azure Static Web Apps.
* Data: `pokemon.json` file and local `pokemon.db` database (created automatically/by scripts).

## Installation

Requirements: Python 3.11+ (3.13 recommended), Node.js 18+.

1. Clone and create Python virtual environment

```powershell
cd D:\Programowanie\Pokemon
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Initialize the database and load data

```powershell
python -m backend.scripts.init_db
python -m backend.scripts.load_data
```

3. Install frontend dependencies

```powershell
cd frontend
npm install
```

## Usage

### Live Deployment

#### Azure

![azure-resource](img\azure.png)

#### Website

![azure-resource](img\website.png)

### Local Development

Run backend (default on `http://127.0.0.1:8000`):

```powershell
uvicorn backend.main:app --reload
```

Available endpoints:

* `GET /` – status and list of available paths
* `GET /health` – simple healthcheck
* `GET /api/v1/summary/` – data summary
* `GET /api/v1/pokemon/` – table/list with filtering and sorting (parameters in `PokemonQueryParams`)
* `GET /api/v1/details/{name}` – details for a given Pokémon

Run frontend in a second terminal (default `http://localhost:5173`):

```powershell
cd frontend
npm run dev
```

## Structure

```
Pokemon/
├── backend/
│   ├── main.py                # FastAPI app, router registration
│   ├── db.py                  # SQLite config (engine, sessions)
│   ├── model/
│   │   ├── sql_model.py       # SQLModel models (ORM)
│   │   └── schema.py          # Pydantic schemas (API I/O)
│   ├── service/
│   │   ├── pokemon_service.py
│   │   ├── pokemon_details_service.py
│   │   └── summary_service.py
│   ├── web/
│   │   ├── pokemon_router.py  # /api/v1/pokemon
│   │   ├── pokemon_details.py # /api/v1/details
│   │   └── summary_router.py  # /api/v1/summary
│   ├── scripts/
│   │   ├── init_db.py         # Create tables
│   │   └── load_data.py       # Import from pokemon.json
│   └── tests/
│       └── test_database.py
├── frontend/
│   ├── index.html
│   ├── vite.config.ts
│   ├── package.json
│   └── src/
│       ├── App.vue
│       ├── main.ts
│       ├── router/
│       │   └── index.ts
│       ├── pages/
│       ├── components/
│       └── api/
├── pokemon.json               # Data source
├── pokemon.db                 # Database (after initialization)
└── README.md
```
