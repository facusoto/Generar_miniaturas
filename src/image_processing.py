from config import INPUT_IMAGES_PATH, OUTPUT_IMAGES_PATH, BACKGROUND_FRAME_PATH, LOGO_PATH, FONT_PATH
from face_detection import position_face_on_canvas
from proportional_cut import llenar_y_recortar
from program_data import get_program_data
from text_box import draw_adaptive_text_with_background
from PIL import Image, ImageFilter
from image4layer import Image4Layer
from rembg import remove, new_session

width, height = 1280, 720
newsize = (width, height)


def get_image_path(image_name: str):
    """
    Retorna la ruta completa de una imagen en el directorio INPUT_IMAGES_PATH
    """
    image = INPUT_IMAGES_PATH / image_name
    if not image.exists():
        raise FileNotFoundError(f"La imagen '{image_name}' no existe en {INPUT_IMAGES_PATH}")

    return image


# def process_image(image_name: str, program, title):
def process_image(image_name: str, title):
    """
    Abre y procesa la imagen especificada
    """
    image_path = get_image_path(image_name)

    image_frame = process_background(image_path)
    image_people = process_people(image_path, OUTPUT_IMAGES_PATH / "gente.png")
    image_people = image_people.convert("RGBA").resize(newsize)

    # Mezcla las personas con el fondo
    image_back_people = Image.alpha_composite(image_frame, image_people)

    # Agrega los logos
    image_logos = add_logos(image_back_people, LOGO_PATH)

    # Agrega el texto
    image_text = add_text(image_logos, title)

    # Guardar la imagen final
    image_text.save(OUTPUT_IMAGES_PATH / "resultado.png")


def process_background(image_path):
    print('Trabajando en la imágen de fondo.')

    # Cargar la imagen y procesarla
    image = Image.open(image_path).convert("RGBA")
    image = llenar_y_recortar(image, width, height)

    # Agregar efecto blur
    image_blur = image.filter(ImageFilter.GaussianBlur(radius = 10))

    # Crear una imagen de color sólido para hacer overlay
    background_color = Image.new('RGBA', (width, height), (40, 90, 215))

    # Hace el blend entre las dos imagenes
    image_blend = Image4Layer.screen(background_color, image_blur)

    # Agrega el marco
    frame = Image.open(BACKGROUND_FRAME_PATH).convert("RGBA")
    image_frame = Image.alpha_composite(image_blend, frame)

    return image_frame


def process_people(input_path, output_path):
    print("Recortando el fondo, esto puede tardar.")

    # Recortar a la persona y guardar el "resultado crudo"
    input = Image.open(input_path).convert("RGBA")#.resize(newsize)
    my_session = new_session("birefnet-general")
    output = remove(input, session=my_session)
    output.save(output_path)

    # Posicionar caras en el canvas
    print("Ubicando a la persona en la imágen")
    positioned_faces = position_face_on_canvas(output, 2)

    return positioned_faces


# def add_logos(input_image, path, program_logo):
def add_logos(input_image, path):
    print("Agregando los logos")
    logo_reyes = Image.open(LOGO_PATH).convert("RGBA")

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
     