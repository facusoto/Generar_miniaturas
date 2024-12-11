from PIL import Image

# Función simple para llenar el canvas centrando y recortando la imagen
def llenar_y_recortar(imagen_path, canvas_width, canvas_height):
    # Abrir la imagen
    imagen = imagen_path.convert("RGBA")
    
    # Calcular las proporciones de la imagen y del canvas
    imagen_ratio = imagen.width / imagen.height
    canvas_ratio = canvas_width / canvas_height
    
    # Escalar la imagen según el lado más corto
    if canvas_ratio > imagen_ratio:
        # El canvas es más ancho, escalar usando la altura
        nuevo_alto = canvas_height
        nuevo_ancho = int(canvas_height * imagen_ratio)
    else:
        # El canvas es más alto, escalar usando el ancho
        nuevo_ancho = canvas_width
        nuevo_alto = int(canvas_width / imagen_ratio)
    
    imagen_escalada = imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
    
    # Recortar el exceso para que la imagen encaje perfectamente
    left = (imagen_escalada.width - canvas_width) // 2
    top = (imagen_escalada.height - canvas_height) // 2
    right = left + canvas_width
    bottom = top + canvas_height
    
    imagen_recortada = imagen_escalada.crop((left, top, right, bottom))
    
    return imagen_recortada
