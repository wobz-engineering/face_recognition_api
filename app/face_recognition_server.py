import os
from flask import Flask, jsonify, request, redirect
import face_recognition
import ast

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/generate-encodings', methods=['POST'])
def post_generate_encodings():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return get_faces_encodings(file)

def get_faces_encodings(file_stream):
    img = face_recognition.load_image_file(file_stream)
    unknown_face_encodings = face_recognition.face_encodings(img)

    result = {
        "face_detected": False,
        "encodings": []
    }

    if(len(unknown_face_encodings) > 0):
        result = {
            "face_detected": True,
            "encodings": list(unknown_face_encodings[0])
        }

    return jsonify(result)

@app.route('/compare-faces', methods=['POST'])
def post_compare_faces():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        encodings = request.form.get('encodings')
        encodings = ast.literal_eval(encodings)

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            return compare_faces(encodings, file)

def compare_faces(original_encodings, file_stream):
    img = face_recognition.load_image_file(file_stream)
    unknown_face_encodings = face_recognition.face_encodings(img)

    result = {
        "face_detected": False,
        "result": False,
    }

    if len(unknown_face_encodings) > 0:
        is_match = False
        match_results = face_recognition.compare_faces([original_encodings], unknown_face_encodings[0])
        if match_results[0]:
            is_match = True
        result = {
            "face_detected": True,
            "result": is_match
        }

    return jsonify(result)

PORT = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    app.run(threaded=True,host='0.0.0.0',port=PORT)
