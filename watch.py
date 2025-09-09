import os
import pyautogui
from PIL import Image, ImageGrab
import easyocr
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time
import numpy as np

# Función para capturar una captura de pantalla completa
def take_screenshot(file_path):
    screen_width, screen_height = pyautogui.size()
    screenshot = ImageGrab.grab(bbox=(0, 0, screen_width, screen_height))  # Captura de pantalla completa
    screenshot.save(file_path)
    print(f"Captura de pantalla guardada en {file_path}")
    return file_path

# Función para extraer texto de la mitad inferior de una imagen
def extract_text_from_image(image_path):
    reader = easyocr.Reader(['ja'])  # Soporte para japonés
    screen_width, screen_height = pyautogui.size()

    # Cargar la imagen completa y recortar la mitad inferior
    image = Image.open(image_path)
    bottom_half = image.crop((0, screen_height // 2, screen_width, screen_height))

    # Convertir la mitad inferior a una matriz NumPy
    bottom_half_np = np.array(bottom_half)

    # Extraer texto solo de la mitad inferior
    result = reader.readtext(bottom_half_np)
    extracted_text = '\n'.join([text[1] for text in result])
    return extracted_text

# Función para verificar si el primer carácter del texto ha cambiado
def has_text_changed(prev_text, current_text):
    return prev_text[:1] != current_text[:1]  # Compara solo el primer carácter

# Función para crear un PDF con las imágenes guardadas (completas)
def create_pdf_with_images(images, pdf_output_path):
    if not images:
        print("No hay imágenes para agregar al PDF.")
        return

    # Obtener las dimensiones de la primera imagen para ajustar el tamaño del PDF
    first_image = Image.open(images[0])
    img_width, img_height = first_image.size

    # Crear un PDF con el tamaño de la primera imagen
    c = canvas.Canvas(pdf_output_path, pagesize=(img_width, img_height))
    
    for image_path in images:
        img = Image.open(image_path)
        c.drawImage(image_path, x=0, y=0, width=img_width, height=img_height)
        c.showPage()  # Añadir nueva página

    c.save()
    print(f"PDF creado con éxito en {pdf_output_path}")

# Configuración inicial
interval = 3 * 60  # Tiempo total en segundos (10 minutos)
screenshot_interval = 0  # Intervalo entre capturas en segundos
image_folder = "capturas/"
pdf_output = "output_manga_style.pdf"

# Crear la carpeta si no existe
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

captured_images = []
prev_text = ""

start_time = time.time()
while time.time() - start_time < interval:
    file_path = f"{image_folder}screenshot_{int(time.time())}.png"
    
    # Tomar la captura de pantalla completa
    file_path = take_screenshot(file_path)
    
    # Extraer texto solo de la mitad inferior de la imagen
    current_text = extract_text_from_image(file_path)
    
    # Verificar si el primer carácter del texto ha cambiado y guardar la imagen completa si es así
    if has_text_changed(prev_text, current_text):
        captured_images.append(file_path)
        prev_text = current_text

    # Esperar antes de la siguiente captura
    time.sleep(screenshot_interval)

# Crear el PDF con las capturas de pantalla guardadas (completas)
if captured_images:
    create_pdf_with_images(captured_images, pdf_output)
else:
    print("No se detectaron cambios en los subtítulos, no se generó el PDF.")