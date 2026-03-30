import os
import json

base_dir = os.path.dirname(__file__)
ruta = os.path.join(base_dir, "..", "dashboard", "data", "datos.json")
ruta = os.path.abspath(ruta)

with open(ruta, "r", encoding="utf-8") as f:
    datos = json.load(f)

cofres = set()

for d in datos:
    cofres.add(d["Cofre"])

print("\nCOFRES DETECTADOS:\n")
for c in sorted(cofres):
    print("-", c)