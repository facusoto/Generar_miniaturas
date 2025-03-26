import os
import numpy as np
import mediapipe as mp
import math
import logging
from .config import WIDTH, HEIGHT
from PIL import Image

# Configuración de Mediapipe
def setup_mediapipe():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    os.environ["OPENCV_LOG_LEVEL"] = "SILENT"
    os.environ["GLOG_minloglevel"] = "2"
    logging.getLogger().setLevel(logging.ERROR)

    mp_face_mesh = mp.solutions.face_mesh
    return mp_face_mesh.FaceMesh(refine_landmarks=True, static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

# Obtener landmarks
def get_landmarks(image_pillow, face_mesh):
    image_rgba = np.array(image_pillow.convert("RGBA"))
    results = face_mesh.process(image_rgba[..., :3])

    if not results.multi_face_landmarks:
        raise Exception("No se detectó ninguna cara.")
    return results.multi_face_landmarks[0].landmark, image_rgba.shape[:2]

# Procesar imagen original y volteada
def process_image(image_pillow, face_mesh):
    original_landmarks, (h, w) = get_landmarks(image_pillow, face_mesh)

    flipped_image = image_pillow.transpose(Image.FLIP_LEFT_RIGHT)
    flipped_landmarks, _ = get_landmarks(flipped_image, face_mesh)

    return (image_pillow, original_landmarks), (flipped_image, flipped_landmarks), (h, w)

# Detectar orientación considerando inclinación
def detect_face_orientation(landmarks, num_images, current_index):
    # Puntos de referencia
    forehead = landmarks[10]
    chin = landmarks[200]

    # Calcular el ángulo de inclinación
    dx = chin.x - forehead.x
    dy = chin.y - forehead.y
    angle_radians = math.atan2(dy, dx)
    angle_degrees = math.degrees(angle_radians)

    # Rotar temporalmente los puntos clave
    def rotate_point(x, y, angle, cx, cy):
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        nx = cos_a * (x - cx) - sin_a * (y - cy) + cx
        ny = sin_a * (x - cx) + cos_a * (y - cy) + cy
        return nx, ny

    # Centro de rotación
    cx, cy = forehead.x, forehead.y

    # Puntos ajustados
    eye_left_x, _ = rotate_point(landmarks[33].x, landmarks[33].y, -angle_radians, cx, cy)
    eye_right_x, _ = rotate_point(landmarks[263].x, landmarks[263].y, -angle_radians, cx, cy)
    nose_x, _ = rotate_point(landmarks[1].x, landmarks[1].y, -angle_radians, cx, cy)

    # Determinar orientación
    eye_center_x = (eye_left_x + eye_right_x) / 2

    if nose_x < eye_center_x:
        orientation = "izquierda"
    elif nose_x > eye_center_x:
        orientation = "derecha"
    else:
        orientation = "centro"

    # Reglas especiales para el centro
    if current_index == num_images // 2 and orientation == "centro":
        orientation = np.random.choice(["izquierda", "derecha"])

    print(f"Ángulo de inclinación: {angle_degrees:.2f}° - Orientación: {orientation}")
    return orientation

# Mejor orientación según la posición en el canvas
def detect_best_orientation(original_data, flipped_data, image_width, image_height, current_index, num_images):
    original_image, original_landmarks = original_data
    flipped_image, flipped_landmarks = flipped_data

    original_orientation = detect_face_orientation(original_landmarks, image_width, image_height, num_images, current_index)
    flipped_orientation = detect_face_orientation(flipped_landmarks, image_width, image_height, num_images, current_index)

    if current_index <= num_images // 2:
        return (original_image, original_landmarks) if original_orientation != "izquierda" else (flipped_image, flipped_landmarks)
    else:
        return (original_image, original_landmarks) if original_orientation != "derecha" else (flipped_image, flipped_landmarks)

# Posicionar imágenes en el canvas
def position_images_on_canvas(image_pillow, landmarks, canvas, canvas_subdivisions, index, target_eye_center):
    w, h = image_pillow.size

    eye_left = [landmarks[33].x * w, landmarks[33].y * h]
    eye_right = [landmarks[263].x * w, landmarks[263].y * h]
    mouth = [landmarks[13].x * w, landmarks[13].y * h]
    eye_center = [(eye_left[0] + eye_right[0]) / 2, (eye_left[1] + eye_right[1]) / 2]

    eye_to_mouth_dist = math.sqrt((eye_center[0] - mouth[0]) ** 2 + (eye_center[1] - mouth[1]) ** 2)
    natural_dist = 80
    scale = natural_dist / eye_to_mouth_dist

    offset_x = target_eye_center[0] - eye_center[0] * scale
    offset_y = target_eye_center[1] - eye_center[1] * scale

    new_size = (int(w * scale), int(h * scale))
    resized_image = image_pillow.resize(new_size)
    mask = resized_image.split()[3]

    canvas.paste(resized_image, (int(offset_x), int(offset_y)), mask)

# Función principal
def position_face_on_canvas(image_pillow, people_amount):
    face_mesh = setup_mediapipe()
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 0))
    subdivisions = people_amount + 1

    original_data, flipped_data, (h, w) = process_image(image_pillow, face_mesh)

    for i in range(1, people_amount + 1):
        target_eye_center = ((WIDTH // subdivisions) * i, HEIGHT // 3)
        best_image, best_landmarks = detect_best_orientation(original_data, flipped_data, w, h, i, people_amount)

        position_images_on_canvas(best_image, best_landmarks, canvas, subdivisions, i, target_eye_center)

    return canvas
