import tkinter as tk
import threading
import time
import pyautogui
from mss import mss
import numpy as np
import cv2
import pytesseract
import csv
import os
from datetime import datetime

# ----------------------------
# CONFIGURACIÓN
# ----------------------------

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

base_dir = os.path.dirname(__file__)
ruta_imagen = os.path.join(base_dir, "boton_cofre.png")

archivo_csv = "C:/Users/netti/OneDrive/Escritorio/proyecto_cofres_analisis/data/registro_cofres.csv"

# Variable global de control
corriendo = False

# ----------------------------
# ARCHIVO CSV
# ----------------------------

if not os.path.exists(archivo_csv):
    with open(archivo_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Fecha", "Jugador", "Cofre"])

# ----------------------------
# TEMPLATE
# ----------------------------

boton_template = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)

# ----------------------------
# FUNCIONES OCR
# ----------------------------

def preparar_para_ocr(img):
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gris, 150, 255, cv2.THRESH_BINARY)
    return thresh

def boton_presente(imagen_boton):
    gris = cv2.cvtColor(imagen_boton, cv2.COLOR_BGR2GRAY)
    resultado = cv2.matchTemplate(gris, boton_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(resultado)
    return max_val > 0.7

# ----------------------------
# MOTOR PRINCIPAL
# ----------------------------

def recolectar(duracion=None):
    global corriendo

    sct = mss()

    monitor_boton = {"left": 1017, "top": 265, "width": 103, "height": 31}
    monitor_jugador = {"left": 536, "top": 240, "width": 405, "height": 20}
    monitor_cofre = {"left": 561, "top": 258, "width": 384, "height": 37}

    inicio = time.time()

    while corriendo:

        # ⏱️ AUTO STOP
        if duracion and (time.time() - inicio > duracion):
            print("⏱️ Auto-stop")
            break

        img_boton = np.array(sct.grab(monitor_boton))
        boton_np = cv2.cvtColor(img_boton, cv2.COLOR_BGRA2BGR)

        if boton_presente(boton_np):

            pyautogui.click(1068, 280)
            time.sleep(0.35)

            # OCR
            img_jugador = np.array(sct.grab(monitor_jugador))
            img_cofre = np.array(sct.grab(monitor_cofre))

            jugador_np = cv2.cvtColor(img_jugador, cv2.COLOR_BGRA2BGR)
            cofre_np = cv2.cvtColor(img_cofre, cv2.COLOR_BGRA2BGR)

            jugador_procesado = preparar_para_ocr(jugador_np)
            cofre_procesado = preparar_para_ocr(cofre_np)

            config = "--psm 7 -l spa"

            nombre = pytesseract.image_to_string(jugador_procesado, config=config)
            cofre = pytesseract.image_to_string(cofre_procesado, config=config)

            nombre = nombre.strip().lower()
            cofre = cofre.strip().lower()

            # ❌ FILTRO ANTI-BASURA
            if not nombre or not cofre or len(nombre) <= 1:
                continue

            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(archivo_csv, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow([fecha, nombre, cofre])

            print("✔", nombre, "-", cofre)

        time.sleep(0.2)

    corriendo = False
    print("⛔ detenido")

# ----------------------------
# CONTROLES
# ----------------------------

def iniciar():
    global corriendo
    if not corriendo:
        corriendo = True
        threading.Thread(target=recolectar).start()

def detener():
    global corriendo
    corriendo = False

def iniciar_auto():
    global corriendo
    if not corriendo:
        corriendo = True
        threading.Thread(target=recolectar, args=(5,)).start()

# ----------------------------
# UI
# ----------------------------

ventana = tk.Tk()
ventana.title("Recolector de Cofres")

tk.Button(ventana, text="START", width=20, command=iniciar).pack(pady=5)
tk.Button(ventana, text="STOP", width=20, command=detener).pack(pady=5)
tk.Button(ventana, text="AUTO (5s)", width=20, command=iniciar_auto).pack(pady=5)

ventana.mainloop()