from image_processing import process_background as pb
from flask import Flask, request, send_file, render_template
from rembg import remove, new_session
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Asegúrate de que el HTML está en la carpeta 'templates'

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    file = request.files['image']
    input_image = file.read()
    print("Se obtuvo una imagen, procesando")

    my_session = new_session("birefnet-general")
    output = remove(input_image, session=my_session)
    output_image = BytesIO(output)
    output_image.seek(0)

    print("Ya se proceso la imagen")
    return send_file(output_image, mimetype='image/png')

@app.route('/process-background', methods=['POST'])
def process_background():
    file = request.files['image']
    print("Se obtuvo una imagen de fondo, procesando")

    # Procesar la imagen con tu función
    background_image = pb(file)

    # Guardar la imagen en un objeto BytesIO
    output_image = BytesIO()
    background_image.save(output_image, format="PNG")  # Asegúrate de usar el formato adecuado
    output_image.seek(0)

    print("Ya se procesó el fondo")

    return send_file(output_image, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)