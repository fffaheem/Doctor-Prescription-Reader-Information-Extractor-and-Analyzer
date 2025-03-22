import os
from ai import generate 
from flask import Flask, request, jsonify

app = Flask(__name__)

# API Endpoint for prescription extraction
@app.route("/extract-prescription/", methods=["POST"])
def extract_prescription():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save uploaded file temporarily
    temp_filepath = f"temp_{file.filename}"
    file.save(temp_filepath)

    # Process the image
    extracted_data = generate(temp_filepath)

    # Delete temp file after processing
    os.remove(temp_filepath)

    return jsonify(extracted_data)  # Return extracted data as JSON

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)