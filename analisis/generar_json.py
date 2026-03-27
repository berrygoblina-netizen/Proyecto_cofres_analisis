import pandas as pd
import json

import os

base_dir = os.path.dirname(__file__)

ruta_csv = os.path.join(base_dir, "..", "data", "registro_cofres.csv")
ruta_json = os.path.join(base_dir, "..", "data", "datos.json")
print("Buscando CSV en:", ruta_csv)
df = pd.read_csv(ruta_csv, sep=";")
# 🔥 eliminar filas con datos vacíos
df = df.dropna(subset=["Jugador", "Cofre"])

# 🔥 eliminar strings vacíos o basura
df = df[df["Jugador"].str.strip() != ""]
df = df[df["Cofre"].str.strip() != ""]

# convertir a lista de diccionarios
datos = df.to_dict(orient="records")

with open(ruta_json, "w", encoding="utf-8") as f:
    json.dump(datos, f, indent=4, ensure_ascii=False)

print("JSON generado")