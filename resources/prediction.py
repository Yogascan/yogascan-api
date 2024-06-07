from flask import Flask, jsonify, request
import os
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from io import BytesIO
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
app.config["ALLOWED_EXTENSIONS"] = {'png', 'jpg', 'jpeg'}
app.config['LABELS_FILE'] = "./label.txt"

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

# Load the model and labels
model = load_model("yogapose.keras", compile=False)
with open(app.config['LABELS_FILE'], 'r') as file:
    labels = file.read().splitlines()

class Predict(Resource):
    def post(self):
        image = request.files.get("image")
        if image and allowed_file(image.filename):
            # Read image as bytes
            image_bytes = image.read()
            
            # Preprocess image
            img = Image.open(BytesIO(image_bytes)).convert("RGB")
            img = img.resize((224, 224))
            img_array = np.asarray(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array.astype(np.float32) / 255.0

            # Make prediction
            prediction = model.predict(img_array)
            index = np.argmax(prediction)
            class_name = labels[index]
            confidence_score = prediction[0][index]

            return jsonify({
                "status": {
                    "code": 200,
                    "message": "Success predicting",
                },
                "data": {
                    "prediction": class_name,
                    "confidence": float(confidence_score)
                }
            })
        else:
            return jsonify({
                "status": {
                    "code": 400,
                    "message": "Bad request"
                },
                "data": None
            })

# Register the resource
api.add_resource(Predict, '/predict')

if __name__ == '__main__':
    app.run(debug=True)
