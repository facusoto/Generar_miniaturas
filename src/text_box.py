from PIL import Image, ImageDraw, ImageFont

def draw_adaptive_text_with_background(input_image, text, box, font_path, max_font_size, text_color="black", bg_color="yellow", padding=5):
    """
    Dibuja texto adaptativo dentro de un recuadro con un fondo de color sobre una imagen transparente,
    y lo combina con la imagen original.

    :param input_image: Imagen PIL.Image ya abierta sobre la que se combinará el texto.
    :param text: Texto a dibujar.
    :param box: Tupla (x, y, width, height) que define el recuadro donde debe ir el texto.
    :param font_path: Ruta al archivo de la fuente.
    :param max_font_size: Tamaño máximo de la fuente.
    :param text_color: Color del texto.
    :param bg_color: Color de fondo detrás de cada línea de texto.
    :param padding: Espacio adicional (en píxeles) alrededor de cada línea de texto.
    :return: La imagen con el texto combinado.
    """
    # Asegurarnos de que la imagen original tenga un canal alpha
    if input_image.mode != "RGBA":
        input_image = input_image.convert("RGBA")

    # Crear una nueva imagen transparente del mismo tamaño
    overlay = Image.new("RGBA", input_image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    x, y, width, height = box

    # Encontrar el tamaño adecuado de la fuente
    font_size = max_font_size
    font = ImageFont.truetype(font_path, font_size)
    while font_size > 10:
        lines = []
        words = text.split()
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            line_width = draw.textlength(test_line, font=font)
            if line_width <= width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)  # Última línea

        line_height = font_size
        text_height = line_height * len(lines)

        if text_height <= height:
            break
        else:
            font_size -= 1
            font = ImageFont.truetype(font_path, font_size)

    if font_size <= 10:
        raise ValueError("El texto no cabe dentro del recuadro incluso con la fuente mínima.")

    # Dibujar el texto con fondo adaptativo en la capa transparente
    y_offset = y + (height - text_height) // 2
    for line in lines:
        line_width = draw.textlength(line, font=font)
        x_offset = x + (width - line_width) // 2

        # Dibujar fondo detrás de cada línea
        background_box = [
            x_offset - padding,
            y_offset - padding,
            x_offset + line_width + padding,
            y_offset + font_size + padding,
        ]
        draw.rectangle(background_box, fill=bg_color)

        # Dibujar el texto encima del fondo
        draw.text((x_offset, y_offset), line, font=font, fill=text_color)
        y_offset += font_size + padding

    # Combinar la capa con la imagen original
    combined_image = Image.alpha_composite(input_image, overlay)
    return combined_image
