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

import sys

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

ruta_imagen = os.path.join(base_dir, "boton_cofre.png")

archivo_csv = r"C:\Users\netti\OneDrive\Escritorio\Proyecto_cofres_analisis\data\registro_cofres.csv"

tesseract_path = os.path.join(base_dir, "Tesseract-OCR", "tesseract.exe")

if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    pytesseract.pytesseract.tesseract_cmd = r"C:\Tesseract-OCR\tesseract.exe"
contador_cofres = 0
# Variable global de control
corriendo = threading.Event()

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
if boton_template is None:
    print(f"Error: No se pudo cargar el template '{ruta_imagen}'. Asegúrate de que el archivo existe.")
    exit(1)

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

    monitor_boton = {'left': 1129, 'top': 325, 'width': 123, 'height': 47}
    monitor_jugador = {'left': 654, 'top': 306, 'width': 400, 'height': 23}
    monitor_cofre = {'left': 680, 'top': 329, 'width': 438, 'height': 22}

    inicio = time.time()
    ultimo_visto = time.time()  # 👈 NUEVO

    while corriendo.is_set():

        # ⏱️ AUTO STOP por duración
        if duracion and (time.time() - inicio > duracion):
            print("⏱️ Auto-stop por duración")
            break

        print("Capturando imagen del botón...")
        img_boton = np.array(sct.grab(monitor_boton))
        boton_np = cv2.cvtColor(img_boton, cv2.COLOR_BGRA2BGR)
        actualizar_estado("🟡 Buscando...")

        if boton_presente(boton_np):
            ultimo_visto = time.time()  # 👈 RESETEA contador
            actualizar_estado("🟢 Recolectando...")

            print("Botón detectado, haciendo clic en (1191, 351)")
            pyautogui.click(1191, 351)
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

            if not nombre or not cofre or len(nombre) <= 1:
                print(f"Filtro activado: nombre='{nombre}', cofre='{cofre}'")
                continue

            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(archivo_csv, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow([fecha, nombre, cofre])
                sumar_cofre()
            print("✔", nombre, "-", cofre)

        else:
            print("Botón no detectado")
            tiempo_sin_ver = time.time() - ultimo_visto  # 👈 CALCULA tiempo sin ver
            
            actualizar_estado(f"🟠 Sin botón ({round(tiempo_sin_ver,1)}s)")
            # ⏳ CONTROL DE INACTIVIDAD
            
            actualizar_estado("⛔ Detenido")

            if tiempo_sin_ver > 10:
                print("⛔ 10 segundos sin detectar el botón → auto stop")
                break

        corriendo.wait(0.2)

    corriendo.clear()
    print("⛔ detenido")
    actualizar_estado("⛔ Detenido")
# ----------------------------
# CONTROLES
# ----------------------------

def iniciar():
    global corriendo
    if not corriendo.is_set():
        corriendo.set()
        threading.Thread(target=recolectar).start()

def detener():
    global corriendo
    corriendo.clear()

def iniciar_auto():
    global corriendo
    if not corriendo.is_set():
        corriendo.set()
        threading.Thread(target=recolectar, args=(5,)).start()

def actualizar_estado(texto):
    global estado_label
    estado_label.config(text=texto)
    ventana.update_idletasks()

def sumar_cofre():
    global contador_cofres, contador_label
    contador_cofres += 1
    contador_label.config(text=f"Cofres: {contador_cofres}")

# ----------------------------
# UI
# ----------------------------

ventana = tk.Tk()
ventana.title("Recolector de Cofres")
ventana.geometry("320x250")
ventana.configure(bg="#1e1e1e")

COLOR_FONDO = "#1e1e1e"
COLOR_TEXTO = "#ffffff"

# 🏷️ título
titulo = tk.Label(
    ventana,
    text="Recolector de Cofres",
    font=("Arial", 16, "bold"),
    bg=COLOR_FONDO,
    fg=COLOR_TEXTO
)
titulo.pack(pady=10)

# 📊 estado
estado_label = tk.Label(
    ventana,
    text="⛔ Detenido",
    font=("Arial", 11),
    bg=COLOR_FONDO,
    fg="#bbbbbb"
)
estado_label.pack(pady=5)

# 🔢 contador
contador_label = tk.Label(
    ventana,
    text="Cofres: 0",
    font=("Arial", 14, "bold"),
    bg=COLOR_FONDO,
    fg="#4CAF50"
)
contador_label.pack(pady=10)

# 🔘 botones
btn_start = tk.Button(
    ventana,
    text="START",
    width=15,
    height=2,
    bg="#4CAF50",
    fg="white",
    bd=0,
    command=iniciar
)
btn_start.pack(pady=8)

btn_stop = tk.Button(
    ventana,
    text="STOP",
    width=15,
    height=2,
    bg="#E53935",
    fg="white",
    bd=0,
    command=detener
)
btn_stop.pack(pady=5)

ventana.mainloop()
