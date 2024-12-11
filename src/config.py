from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Rutas relativas a carpetas
INPUT_PATH = BASE_DIR / "data" / "inputs"
INPUT_IMAGES_PATH = BASE_DIR / "data" / "inputs" / "fondos"
INPUT_FACES_PATH = BASE_DIR / "data" / "inputs" / "caras"
OUTPUT_PATH = BASE_DIR / "data" / "outputs"
OUTPUT_IMAGES_PATH = BASE_DIR / "data" / "outputs" / "png"
DATABASE_PATH = BASE_DIR / "data" / "base_datos"

# Rutas relativas a imágenes o archivos
BACKGROUND_FRAME_PATH = INPUT_PATH / "graficos" / "marco.png"
LOGO_PATH = INPUT_PATH / "graficos" / "logo.png"
FONT_PATH = INPUT_PATH / "graficos" / "sequel-100-black-65.ttf"