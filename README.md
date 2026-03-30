-Clan Analytics Dashboard

Sistema de automatización y análisis de datos para el seguimiento de actividad en clanes de videojuegos.

-Descripción

Este proyecto permite recolectar, procesar y visualizar datos de jugadores a partir de la recolección de cofres dentro de un juego.

El sistema automatiza la captura de datos, los transforma en información útil y los presenta en un dashboard interactivo.

-Cómo funciona

El sistema está dividido en tres partes:

1. Automatización (Python + OCR)
Detecta cofres en pantalla
Extrae información automáticamente
Guarda los datos en un archivo CSV

2. Procesamiento de datos
Convierte los datos en formato estructurado
Calcula métricas como semanas y puntos
Genera un archivo JSON

3. Visualización (Dashboard)
Muestra rankings de jugadores
Permite filtrar por semana
Presenta estadísticas de forma clara

Problema que resuelve

En muchos juegos, el seguimiento de la actividad de los jugadores es manual y poco claro.

Este proyecto automatiza ese proceso, facilitando el análisis del rendimiento y la toma de decisiones dentro del clan.

Tecnologías utilizadas

Python (automatización y procesamiento)
OpenCV / OCR
HTML, CSS, JavaScript
JSON / CSV

Estructura del proyecto

project/
│
├── dashboard/      # interfaz web
├── automation/     # captura de datos (OCR)
├── analysis/       # procesamiento de datos
├── data/           # archivos CSV
└── README.md

Cómo usar el proyecto

-Ejecutar la automatización:

python automation/cofre_auto.py

-Procesar los datos:

python analysis/generar_json.py

-Abrir el dashboard:

dashboard/index.html

📸 Demo

(Agregar capturas del dashboard)

-Sobre mí

Estoy formándome como Data Analyst y desarrollo proyectos prácticos que combinan automatización, análisis y visualización de datos.

Este proyecto forma parte de mi portfolio.