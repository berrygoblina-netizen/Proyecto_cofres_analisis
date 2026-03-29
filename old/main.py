import pandas as pd
import json
import os
from datetime import datetime
# BLOQUE 0: FUNCIONES (cerebro del sistema)


def cargar_valores_cofres(ruta="valores_cofres.json"):
    if os.path.exists(ruta):
        with open(ruta, "r") as f:
            return json.load(f)
    else:
        return {}

def guardar_valores_cofres(valores, ruta="valores_cofres.json"):
    with open(ruta, "w") as f:
        json.dump(valores, f, indent=4)

def obtener_metricas(df, jugador, semana="Todas"):
    
    df_jugador = df[df["Jugador"] == jugador]

    if semana != "Todas":
        df_jugador = df_jugador[df_jugador["semana"] == semana]

    cofres = len(df_jugador)
    riqueza = df_jugador["puntos"].sum()

    return cofres, riqueza


def obtener_ranking(df, semana="Todas"):
    
    if semana != "Todas":
        df = df[df["semana"] == semana]

    ranking = (
        df.groupby("Jugador")["puntos"]
        .sum()
        .reset_index()
        .sort_values(by="puntos", ascending=False)
    )

    ranking = ranking[ranking["puntos"] > 0]

    return ranking

def detectar_cofres_nuevos(df, valores_cofres):
    
    cofres_en_datos = set(df["Cofre"].unique())
    cofres_mapeados = set(valores_cofre.keys())

    nuevos = cofres_en_datos - cofres_mapeados

    return nuevos

#BLOQUE 1: Cargar y preparar datos

# 1. Cargar datos
df = pd.read_csv("data/registro_cofres.csv", sep=";")

#1.1 convierte la columna "Fecha" a formato datetime
df["Fecha"] = pd.to_datetime(df["Fecha"])


# 1.2. Ver columnas 
print(df.columns)

#BLOQUE 2: Transformar datos (CREAS INTELIGENCIA)
#FECHA INICIO: para calcular la semana de cada cofre, necesitamos saber cuándo empezó el registro. Esto reemplaza a la función MIN de Excel.
fecha_inicio = df["Fecha"].min()
df["semana"] = ((df["Fecha"] - fecha_inicio).dt.days // 7) + 1
df["semana"] = "Semana " + df["semana"].astype(str)
#VALORES DE LOS COFRES: para calcular la riqueza, necesitamos asignar un valor a cada tipo de cofre. Esto reemplaza a la función BUSCARV de Excel.
valores_cofre = cargar_valores_cofres()
# detectar cofres nuevos
nuevos_cofres = detectar_cofres_nuevos(df, valores_cofre)

if nuevos_cofres:
    print("\n⚠️ Cofres nuevos detectados:")
    for cofre in nuevos_cofres:
        print("-", cofre)
else:
    print("\n✔ Todo esta actualizado")

# mapear cofres nuevos
for cofre in nuevos_cofres:
    valor = input(f"Ingresá el valor para {cofre}: ")
    
    if valor.isdigit():
        valores_cofre[cofre] = int(valor)
    else:
        print("❌ Valor inválido. Se asigna 0")
        valores_cofre[cofre] = 0

if nuevos_cofres:
    guardar_valores_cofres(valores_cofre)
# 2.2. Crear columna  (esto reemplaza BUSCARV)
df.columns = ["fecha", "jugador", "cofre"]
df["fecha"] = pd.to_datetime(df["fecha"])  # asegúrate de que sea datetime
fecha_inicio = df["fecha"].min()
df["semana"] = ((df["fecha"] - fecha_inicio).dt.days // 7) + 1
df["semana"] = "Semana " + df["semana"].astype(str)

registros = df.to_dict(orient="records")

with open("data/datos.json", "w", encoding="utf-8") as f:
    json.dump(registros, f, ensure_ascii=False, indent=4)

# 2.3. Crear columna de puntos (esto reemplaza BUSCARV)
df["puntos"] = df["Cofre"].map(valores_cofre)
df["puntos"] = df["puntos"].fillna(0)

#BLOQUE 3: OPCIONES DEL SISTEMA
# generas las listas (como UNICOS de Excel) para mostrarle al usuario qué opciones tiene. Esto reemplaza a la función UNICOS de Excel.
jugadores = df["Jugador"].unique()

print("\nJugadores disponibles:")
print(jugadores)

# BLOQUE 4: INTERACCIÓN CON EL USUARIO
# 4. input del usuario
jugadores_lower = [j.lower() for j in jugadores]

while True:
    jugador_input = input("\nElegí un jugador: ").strip().lower()

    if jugador_input in jugadores_lower:
        jugador = jugadores[jugadores_lower.index(jugador_input)]
        break
    else:
        print("❌ Ese jugador no existe. Probá de nuevo.")

# 4.5. Lista de semanas disponibles
semanas = df["semana"].unique()

print("\nSemanas disponibles:")
print(semanas)

# input del usuario
semana_input = input("\nElegí una semana (número o 'Todas'): ").strip().lower()

if semana_input == "todas":
    semana = "Todas"
else:
    # si escribe solo número (ej: 2)
    if semana_input.isdigit():
        semana = "Semana " + semana_input
    else:
        # si escribe "semana 2"
        if "semana" in semana_input:
            numero = semana_input.replace("semana", "").strip()
            if numero.isdigit():
                semana = "Semana " + numero
            else:
                print("❌ Formato inválido. Se usará 'Todas'")
                semana = "Todas"
        else:
            print("❌ Formato inválido. Se usará 'Todas'")
            semana = "Todas"

#BLOQUE 5: FILTRAR Y CALCULAR MÉTRICAS
#LOGICA DE DASHBOARD: el usuario elige un jugador y una semana, y el sistema le muestra las métricas correspondientes. Esto reemplaza a las funciones de filtro y cálculo de Excel.

# 5.1 Filtrar datoS

cofres_totales, riqueza_total = obtener_metricas(df, jugador, semana)


#BLOQUE 6: SALIDA(RESULTADOS)
#  Mostrar resultados

print("\nJugador:", jugador)
print("Cofres:", cofres_totales)
print("Riqueza:", riqueza_total)

df_debug = df[df["Jugador"] == jugador]

if semana != "Todas":
    df_debug = df_debug[df_debug["semana"] == semana]

print(df_debug[["Fecha", "semana"]].head())

#BLOQUE 7: RANKING DE JUGADORES
#. Ranking de jugadores
ranking = (
    df.groupby("Jugador")["puntos"]
    .sum()
    .reset_index()
    .sort_values(by="puntos", ascending=False)
)

ranking = ranking[ranking["puntos"] > 0]


#BLOQUE 8: FUNCION DE RANKING
# 8.5. Función de ranking

#BLOQUE 9: USARLO
ranking = obtener_ranking(df, semana)

print("\nRanking limpio:")
print(ranking.head(10))
print("Semana elegida:", semana)