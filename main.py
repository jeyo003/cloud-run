from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import joblib
import os
import traceback

app = Flask(__name__)
CORS(app)  # Allow React Native to access this API

# Load the trained model and scaler with error handling
try:
    model = load_model("phishing.h5")  # Load trained CNN model
    scaler = joblib.load("scaler.pkl")  # Load pre-trained StandardScaler
    print("Model and scaler loaded successfully.")
except Exception as e:
    print("Error loading model or scaler:")
    traceback.print_exc()
    model = None
    scaler = None

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        # Validate JSON input
        if "features" not in data:
            return jsonify({"error": "Missing 'features' key in request"}), 400

        input_data = np.array(data["features"]).reshape(1, 40)  # Ensure shape (1, 40)

        # Check if model and scaler are loaded
        if model is None or scaler is None:
            return jsonify({"error": "Model or scaler not loaded properly"}), 500

        # Apply feature scaling (ensure scaler exists)
        if scaler is not None:
            input_data = scaler.transform(input_data)  # Now shape (1, 40)
        else:
            return jsonify({"error": "Scaler is not available"}), 500

        # Reshape for Conv1D model (samples, timesteps, features)
        input_data = input_data.reshape(1, input_data.shape[1], 1)  # (1, 40, 1)

        # Make prediction
        prediction = model.predict(input_data)[0][0]  # Extract single value

        # Convert to human-readable result
        result = "Phishing" if prediction >= 0.5 else "Legitimate"

        return jsonify({"prediction": float(prediction), "result": result})

    except Exception as e:
        print("Error during prediction:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Default to 8080 for Cloud Run
    app.run(host="0.0.0.0", port=port)
