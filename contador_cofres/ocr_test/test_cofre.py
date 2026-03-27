import cv2
import pytesseract
import csv
import os
from datetime import datetime
import pandas as pd

# --- Configurar ruta de Tesseract ---
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --- Cargar imagen ---
imagen = cv2.imread("captura.png")

# --- Recortes ---
jugador_roi = imagen[240:260, 536:941]
cofre_roi   = imagen[258:295, 561:945]

# --- Preprocesamiento ---
def preparar_para_ocr(img):
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gris, 150, 255, cv2.THRESH_BINARY)
    return thresh

jugador_procesado = preparar_para_ocr(jugador_roi)
cofre_procesado   = preparar_para_ocr(cofre_roi)

# --- OCR ---
config = "--psm 7"

nombre = pytesseract.image_to_string(jugador_procesado, config=config)
cofre  = pytesseract.image_to_string(cofre_procesado, config=config)

# --- Limpieza ---
nombre = nombre.strip().replace("\n", "")
cofre = cofre.strip().replace("\n", "")
cofre = cofre.replace("niveI", "nivel")

print("Jugador:", nombre)
print("Cofre:", cofre)

# --- Guardar registro ---
archivo = "registro_cofres.csv"

# Crear archivo si no existe
if not os.path.exists(archivo):
    with open(archivo, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Fecha", "Jugador", "Cofre"])

# Agregar nuevo registro
fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(archivo, mode="a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([fecha, nombre, cofre])

# --- Mostrar imágenes procesadas ---
cv2.imshow("Jugador procesado", jugador_procesado)
cv2.imshow("Cofre procesado", cofre_procesado)

cv2.waitKey(0)
cv2.destroyAllWindows()

# --- Estadísticas ---
df = pd.read_csv(archivo)
conteo = df["Jugador"].value_counts()

print("\nEstadísticas:")
print(conteo)