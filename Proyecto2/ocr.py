import os
import pytesseract
import pandas as pd
from PIL import Image

# Directorio que contiene las imágenes
directorio = '/home/draco/Descargas/clasismo'

# Lista todos los archivos en el directorio
archivos = os.listdir(directorio)

# Filtra solo los archivos de imagen (puedes ajustar esto según los tipos de archivos que quieras procesar)
imagenes = [archivo for archivo in archivos if archivo.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp'))]
image_names = []
texts = []

# Itera sobre cada imagen
for imagen in imagenes:
    # Construye la ruta completa de la imagen
    ruta_imagen = os.path.join(directorio, imagen)
    
    # Carga la imagen
    img = Image.open(ruta_imagen)
    
    # Realiza OCR en la imagen
    texto = pytesseract.image_to_string(img)
    texto = ' '.join(texto.split())
    
    if (texto):
        image_names.append(imagen)
        texts.append(texto)

# Crea un DataFrame de pandas con los resultados
df = pd.DataFrame({'Nombre de la Imagen': image_names, 'Texto': texts})

# Guarda el DataFrame como un archivo CSV
df.to_csv('resultados_ocr.csv', index=False)

print("Los resultados se han guardado en 'resultados_ocr.csv'")
