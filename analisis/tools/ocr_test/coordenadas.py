import cv2

imagen = cv2.imread("captura.png")

def obtener_coordenadas(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordenadas: {x}, {y}")

cv2.imshow("Imagen", imagen)
cv2.setMouseCallback("Imagen", obtener_coordenadas)

print("Haz clic en la imagen para obtener coordenadas.")
print("Presiona cualquier tecla para salir.")

cv2.waitKey(0)
cv2.destroyAllWindows()