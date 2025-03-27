from image_processing import process_background as pb
from image_processing import remove_bg, remove_extra_canvas
from face_detection import position_face_on_canvas
from flask import Flask, request, send_file, render_template, jsonify
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process-background', methods=['POST'])
def process_background():
    file = request.files['image']
    print("Se obtuvo una imagen de fondo, procesando")

    # Procesar la imagen con tu función
    background_image = pb(file)

    # Guardar la imagen en un objeto BytesIO
    output_image = BytesIO()
    background_image.save(output_image, format="PNG")
    output_image.seek(0)

    print("Ya se procesó el fondo")

    return send_file(output_image, mimetype='image/png')


@app.route('/process-people', methods=['POST'])
def process_people():
    # Obtener la imagen desde el Frond-End
    file = request.files['image']
    input_image = file.read()
    print("Se obtuvo una imagen, procesando")

    # Remover el fondo y recortar el canvas a su mínimo
    removed_background = remove_bg(input_image)
    removed_canvas = remove_extra_canvas(removed_background)
    image_base64 = base64.b64encode(removed_canvas.getvalue()).decode('utf-8')

    image_attributes = position_face_on_canvas(removed_canvas, 1)

    # Construir la respuesta JSON con imagen y datos
    response = {
        "image": image_base64,  # Imagen en base64 para enviar en JSON
        "new_size": image_attributes[0],  # (width, height)
        "offset": image_attributes[1]     # (offset_x, offset_y)
    }

    print("Ya se procesó la imagen y se recortó el canvas al mínimo posible")
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)