import os
from ai import generate 
from flask import Flask, request, jsonify
from PIL import Image
import fitz
import io

app = Flask(__name__)


# Allowed file extensions
ALLOWED_EXTENSIONS = {"jpeg", "jpg", "png", "pdf"}

# Check if uploaded file is valid
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def pdf_to_image(file_path):
    file_ext = file_path.rsplit(".", 1)[1].lower()

    # If the file is a PDF, convert it to an image
    if file_ext == "pdf":
        doc = fitz.open(file_path)
        
        if len(doc) == 0:
            raise ValueError("Empty PDF file or no pages found.")
        
        # Get the first page
        page = doc[0]
        pix = page.get_pixmap()  # Render as an image
        
        # Convert pixmap to PIL Image
        img = Image.open(io.BytesIO(pix.tobytes("ppm")))

        img.save("converted_image.jpg", format="JPEG")

        return "converted_image.jpg"
    return file_path




# API Endpoint for prescription extraction
@app.route("/extract-prescription/", methods=["POST"])
def extract_prescription():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Allowed: jpg, jpeg, png, pdf"}), 400

    # Save uploaded file temporarily
    temp_filepath = f"temp_{file.filename}"
    file.save(temp_filepath)

    # Process the image
    extracted_data = pdf_to_image(temp_filepath)
    try:
        extracted_data = generate(extracted_data)
    except:
        extracted_data = {"error": "API time out"}

    # Delete temp file after processing
    os.remove(temp_filepath)
    try:
        os.remove("converted_image.jpg")
    except:
        ""

    return jsonify(extracted_data)  # Return extracted data as JSON

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)