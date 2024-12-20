from flask import Flask, request, jsonify, render_template
import os
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import cv2
from sklearn.metrics.pairwise import cosine_similarity
from datasets import load_dataset
from google.cloud import vision

# Initialize Flask app
app = Flask(__name__)

# Load model and dataset
MODEL_HANDLE = "https://tfhub.dev/google/imagenet/efficientnet_v2_imagenet21k_ft1k_b0/feature_vector/2"
IMAGE_SIZE = (224, 224)
feature_extractor = hub.KerasLayer(MODEL_HANDLE, trainable=False)
dataset = load_dataset("tonyassi/celebrity-1000", split="train")
df = dataset.to_pandas()
celebrity_features = extract_features_from_dataset(df)

# Google Vision API setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/google/key.json"
client = vision.ImageAnnotatorClient()

# Function to preprocess uploaded image
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = tf.image.resize(image_rgb, IMAGE_SIZE) / 255.0
    return image_resized

@app.route('/celebrity')
def celebrity():
    return render_template('celebrity.html')

# Route for image upload
@app.route("/upload", methods=["POST"])
def upload_image():
    print("sdjnsd")
    app.logger.error("No image field in request files")
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["image"]
    file_path = f"./static/uploads/{file.filename}"
    file.save(file_path)

    app.logger.error("1")
    # Process image and find matches
    input_features = feature_extractor(tf.expand_dims(preprocess_image(file_path), axis=0)).numpy()
    similarities = cosine_similarity(input_features, celebrity_features).flatten()
    top_indices = similarities.argsort()[-5:][::-1]

    app.logger.error("2")
    # Prepare response
    matches = []
    for idx in top_indices:
        row = df.iloc[idx]
        matches.append({
            "name": row["label"],
            "similarity": round(similarities[idx] * 100, 2),
            "image": row["image"]["url"]  # Assume the dataset contains image URLs
        })
    app.logger.error("4")
    return jsonify({"matches": matches})

# Run server
if __name__ == "__main__":
    app.run(debug=True)
