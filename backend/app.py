# ----- REQUIRED IMPORTS -----

from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import numpy as np
import cv2
from PIL import Image
import io
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions

# ----- EXECUTION CODE -----

app = Flask(__name__)
CORS(app)
model = VGG16(weights='imagenet')

@app.route('/api/analyze', methods=['POST'])
def analyze_handwriting():
    data = request.json
    image_data = data['imageData'].split(',')[1]
    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes))
    image = image.resize((224, 224))
    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = preprocess_input(image_array)
    predictions = model.predict(image_array)
    decoded_predictions = decode_predictions(predictions, top=3)[0]
    strokes = data['strokes']
    legibility_score = analyze_legibility(strokes)
    consistency_score = analyze_consistency(strokes)
    total_score = (legibility_score + consistency_score) / 2
    is_cooked = total_score < 60
    return jsonify({
        'legibilityScore': legibility_score,
        'consistencyScore': consistency_score,
        'totalScore': total_score,
        'isCooked': is_cooked,
        'classification': decoded_predictions[0][1],
        'confidence': float(decoded_predictions[0][2])
    })

def analyze_legibility(strokes):
    if not strokes:
        return 0
    total_points = sum(len(stroke) for stroke in strokes)
    stroke_count = len(strokes)
    complexity_score = min(100, (total_points / 10) + (stroke_count * 5))
    return int(complexity_score)

def analyze_consistency(strokes):
    if not strokes or len(strokes) < 2:
        return 50  
    stroke_speeds = []
    for stroke in strokes:
        if len(stroke) < 2:
            continue
        times = [point['time'] for point in stroke]
        time_diffs = [times[i+1] - times[i] for i in range(len(times)-1)]
        if time_diffs:
            stroke_speeds.append(sum(time_diffs) / len(time_diffs))
    if not stroke_speeds:
        return 50
    avg_speed = sum(stroke_speeds) / len(stroke_speeds)
    speed_variations = [abs(speed - avg_speed) for speed in stroke_speeds]
    avg_variation = sum(speed_variations) / len(speed_variations)
    consistency_score = max(0, 100 - (avg_variation / 10))
    return int(consistency_score)

@app.route('/')

def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)