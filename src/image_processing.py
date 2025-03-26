from config import BACKGROUND_FRAME_PATH, CHANNEL_LOGO_PATH, FONT_PATH, WIDTH, HEIGHT
from face_detection import position_face_on_canvas
from program_data import get_program_data
from proportional_cut import llenar_y_recortar
from text_box import draw_adaptive_text_with_background
from image4layer import Image4Layer
from io import BytesIO
from PIL import Image, ImageFilter
from rembg import remove, new_session


def process_background(image_path):
    print('Trabajando en la imágen de fondo.')

    # Cargar la imagen y procesarla
    image = Image.open(image_path).convert("RGBA")
    image = llenar_y_recortar(image, WIDTH, HEIGHT)

    # Agregar efecto blur
    image_blur = image.filter(ImageFilter.GaussianBlur(radius = 10))

    # Crear una imagen de color sólido para hacer overlay
    background_color = Image.new('RGBA', (WIDTH, HEIGHT), (40, 90, 215))

    # Hace el blend entre las dos imagenes
    image_blend = Image4Layer.screen(background_color, image_blur)

    # Agrega el marco
    frame = Image.open(BACKGROUND_FRAME_PATH).convert("RGBA")
    image_frame = Image.alpha_composite(image_blend, frame)

    return image_frame


def remove_bg(input_image):
    my_session = new_session("birefnet-general")
    output = remove(input_image, session=my_session)
    return output


def remove_extra_canvas(removed_background):
    # Convertir la imagen a formato PIL
    image = Image.open(BytesIO(removed_background)).convert("RGBA")

    # Recortar el canvas eliminando píxeles transparentes
    bbox = image.getbbox()
    if bbox:
        image = image.crop(bbox)

    # Guardar la imagen en memoria sin escribir en disco
    output = BytesIO()
    image.save(output, format="PNG")
    output.seek(0)

    return output


def add_logos(input_image):
    print("Agregando los logos")
    logo_reyes = Image.open(CHANNEL_LOGO_PATH).convert("RGBA")

    background_image = input_image.copy()
    background_image.paste(logo_reyes, (1080, 45), logo_reyes)
    # background_image.paste(program_logo, (0, 0), program_logo)

    return background_image


def add_text(back_image, text):
    print("Agregando el texto")

    box = (32, 490, 850, 200)  # x, y, ancho, alto
    font_path = FONT_PATH
    max_font_size = 72

    return draw_adaptive_text_with_background(
        back_image,
        text,
        box,
        font_path,
        max_font_size,
        text_color="white",
        bg_color=(40, 90, 215),
        padding=5
        )
     