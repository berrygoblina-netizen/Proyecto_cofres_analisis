import os
import json
import re

base_dir = os.path.dirname(__file__)
ruta = os.path.join(base_dir, "../data/datos.json")

with open(ruta, "r", encoding="utf-8") as f:
    datos = json.load(f)

jugadores = set()

for d in datos:
    nombre = (d.get("Jugador") or "").strip().lower()

    # 🔥 FILTRO IGUAL QUE JS
    if len(nombre) <= 2:
        continue
    if len(nombre) > 20:
        continue
    if re.match(r'^(.)\1+$', nombre):
        continue
    if not re.match(r'^[a-z0-9\s]+$', nombre):
        continue

    jugadores.add(nombre)

print("\nJUGADORES LIMPIOS:\n")

for j in sorted(jugadores):
    print("-", j)