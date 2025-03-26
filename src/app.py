from image_processing import process_background as pb
from image_processing import remove_bg, remove_extra_canvas
from flask import Flask, request, send_file, render_template
from io import BytesIO

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

    print("Ya se procesó la imagen y se recortó el canvas al mínimo posible")
    return send_file(removed_canvas, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)