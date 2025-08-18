


## Struktura proejktu 
```
Pokemon/
├── backend/                        # Python + FastAPI + SQLModel
│   ├── main.py                    # Tworzy FastAPI app i uruchamia
│   ├── db.py                      # engine + session (sqlite)
│
│   ├── scripts/                   # Skrypty jednorazowe
│   │   ├── init_db.py            # Tworzy bazę danych
│   │   └── load_data.py          # Ładuje dane z pokemon.json do DB
│
│   ├── model/                     # Warstwa danych
│   │   ├── sql_model.py          # SQLModel (ORM)
│   │   └── schema.py             # Pydantic BaseModel (API)
│
│   ├── service/                   # Logika biznesowa
│   │   └── pokemon_service.py    # Filtrowanie, sortowanie, paginacja
│
│   ├── web/                       # FastAPI routers
│   │   └── pokemon_router.py     # Endpointy API
│
│   └── tests/                     # Testy backendu (pytest)
│       └── test_api.py
│
├── frontend/                      # Vue 3 + Vite + TypeScript + Pinia
│   ├── index.html
│   ├── vite.config.ts
│   ├── package.json
│   ├── tsconfig.json
│   ├── public/
│   └── src/
│       ├── App.vue
│       ├── main.ts
│       ├── router/
│       │   └── index.ts          # Vue Router
│       ├── store/
│       │   └── pokemon.ts        # Pinia store
│       ├── pages/
│       │   ├── DashboardPage.vue
│       │   └── PokemonDetails.vue
│       ├── components/
│       │   ├── PokemonTable.vue
│       │   ├── PokemonCard.vue
│       │   └── SummaryCard.vue
│       └── api/
│           └── pokemonApi.ts     # Axios setup
│
├── pokemon.json                   # Dane wejściowe
├── README.md                      # Instrukcja uruchomienia (frontend + backend)
└── .venv/                         # (opcjonalnie, lokalne środowisko Pythona)

```


### generate database  
```cmd
(.venv) PS D:\Programowanie\Pokemon> python -m backend.scripts.init_db
```