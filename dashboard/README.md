# 🛡️ Clan Analytics Dashboard
> **Sistema de automatización y análisis de datos para el seguimiento de actividad en clanes de videojuegos.**

## 📝 Descripción
Este proyecto permite recolectar, procesar y visualizar el desempeño de jugadores a partir de la recolección de cofres. Automatiza la captura de datos, los transforma en información estructurada y los presenta en un **dashboard interactivo** accesible vía web.

## ⚙️ Cómo funciona
El sistema se divide en tres etapas clave:

1. **Automatización (Python + OCR):** Detecta cofres en pantalla, extrae la información automáticamente y la almacena en archivos `CSV`.
2. **Procesamiento de Datos:** Convierte los datos brutos en métricas útiles (puntos por semana, rankings) y genera un archivo `JSON` optimizado.
3. **Visualización (Dashboard):** Una interfaz web dinámica que permite filtrar por semana y visualizar estadísticas claras de cada jugador.

## 🚀 Problema que resuelve
En muchos entornos competitivos, el seguimiento de actividad es **manual y propenso a errores**. Este proyecto elimina esa carga administrativa, facilitando la toma de decisiones basada en datos reales del rendimiento del clan.

## 🛠️ Tecnologías utilizadas
* **Lenguajes:** Python (Backend & Scripting), JavaScript (Frontend).
* **Librerías de Visión:** OpenCV / OCR (Tesseract).
* **Web:** HTML5, CSS3.
* **Formatos de datos:** JSON, CSV.
* **Despliegue:** GitHub Actions & GitHub Pages.

## 📂 Estructura del proyecto
```bash
├── dashboard/     # Interfaz web (Frontend)
├── automation/    # Captura de datos y OCR
├── analisis/      # Scripts de procesamiento y lógica de negocio
├── data/          # Almacenamiento de registros (CSV/JSON)
└── README.md