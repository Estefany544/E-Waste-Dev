from flask import Flask, request, jsonify, send_file
from roboflow import Roboflow
import os

app = Flask(__name__)

# Configuración de Roboflow
API_KEY = "NgUTB1xy6mHUeMCJo33c"
WORKSPACE = "ewaste-ik8z8"
PROJECT = "e-waste-ojvb8"
VERSION = 3

# Inicialización de Roboflow
rf = Roboflow(api_key=API_KEY)
project = rf.workspace(WORKSPACE).project(PROJECT)
model = project.version(VERSION).model

# Rutas de las imágenes
image_path = "C:/temp/temp_image.jpg"  # Asegúrate de que este directorio exista
processed_image_path = "C:/temp/prediction.jpg"

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No se encontró ninguna imagen'}), 400

    # Guardar imagen temporalmente
    image = request.files['image']
    image.save(image_path)

    # Llamar a la API de Roboflow para la inferencia
    response = model.predict(image_path, confidence=40, overlap=30).json()

    # Guardar la imagen procesada con las detecciones visualizadas
    model.predict(image_path, confidence=40, overlap=30).save(processed_image_path)

    # Eliminar la imagen temporal original
    os.remove(image_path)

    # Responder con los datos JSON de detección y la ruta de la imagen procesada
    return jsonify({
        "json_data": response,
        "image_path": processed_image_path
    })

@app.route('/get_image', methods=['GET'])
def get_image():
    if os.path.exists(processed_image_path):
        return send_file(processed_image_path, mimetype='image/jpeg')
    else:
        return jsonify({'error': 'Image not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
