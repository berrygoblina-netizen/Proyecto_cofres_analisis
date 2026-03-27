import cv2
import os
import pytesseract

# 🔹 Configurar ruta a Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Tesseract-OCR\tesseract.exe"

# 🔹 Ruta a imagen de prueba (relativa a este script)
img_path = os.path.join(os.path.dirname(__file__), "captura_info_ejemplo.png")
if not os.path.exists(img_path):
    print(f"❌ No se encuentra la imagen: {img_path}")
    exit()

# 🔹 Cargar imagen y procesar
imagen = cv2.imread(img_path)
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gris, 150, 255, cv2.THRESH_BINARY)

# 🔹 Configuración OCR
config = "--psm 7 -l spa -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÁÉÍÓÚáéíóúÑñ0123456789 "

# 🔹 Ejecutar OCR
texto = pytesseract.image_to_string(thresh, config=config)

print("=== TEXTO DETECTADO ===")
print(texto.strip())