import json
from collections import defaultdict
from pathlib import Path

# Załaduj dane z JSON
with open(Path("pokemon.json"), encoding="utf-8") as f:
    data = json.load(f)

# Szukaj duplikatów
ability_pairs = defaultdict(int)

for p in data:
    number = p["number"]
    abilities = p.get("abilities", [])
    for ability in abilities:
        key = (number, ability)
        ability_pairs[key] += 1

# Wyświetl tylko duplikaty
duplicates = {k: v for k, v in ability_pairs.items() if v > 1}

print("Duplicates (number, ability):")
for (number, ability), count in duplicates.items():
    print(f"Pokemon #{number} has ability '{ability}' {count} duplicated")
