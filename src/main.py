from config import INPUT_IMAGES_PATH, OUTPUT_IMAGES_PATH, DATABASE_PATH
from database import get_program_data
from image_processing import process_image
from pathlib import Path

def main():
    # streaming = input('¿De que programa de streaming se trata?: ')
    title = input('¿Cual es el título del programa?: ')

    # Obtener datos del programa
    # program_name, program_color, program_logo = get_program_data(DATABASE_PATH, streaming)

    # Procesar imágenes
    SAMPLE_IMAGE = INPUT_IMAGES_PATH / "fondo_3.jpg"
    images = process_image(SAMPLE_IMAGE, title)

if __name__ == "__main__":
    main()