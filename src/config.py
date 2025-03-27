from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Rutas relativas a carpetas
INPUT_PATH = BASE_DIR / "data" / "inputs"
DATABASE_PATH = BASE_DIR / "data" / "base_datos"
LOGO_PATH = INPUT_PATH / "graficos" / "logos"

# Rutas relativas a imágenes o archivos
BACKGROUND_FRAME_PATH = INPUT_PATH / "graficos" / "marco.png"
CHANNEL_LOGO_PATH = LOGO_PATH / "logo_reyes.png"
FONT_PATH = INPUT_PATH / "graficos" / "sequel-100-black-65.ttf"

# Tamaño definido para las imagenes
WIDTH, HEIGHT = 1280, 720
EYE_POSITION_Y = 240