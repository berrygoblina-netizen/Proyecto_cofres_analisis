import pyautogui
import time

print("Mueve el mouse al botón y presiona Ctrl+C para detener.")
try:
    while True:
        x, y = pyautogui.position()
        print(f"Posición del mouse: x={x}, y={y}")
        time.sleep(1)
except KeyboardInterrupt:
    print("Calibración detenida.")