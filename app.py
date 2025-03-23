import os
from flask import Flask, request, render_template, jsonify
from PIL import Image
import fitz
import io
from ai import generate

app = Flask(__name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"jpeg", "jpg", "png", "pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def pdf_to_image(file_path):
    file_ext = file_path.rsplit(".", 1)[1].lower()
    if file_ext == "pdf":
        doc = fitz.open(file_path)
        if len(doc) == 0:
            raise ValueError("Empty PDF file or no pages found.")
        page = doc[0]
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("ppm")))
        img.save("converted_image.jpg", format="JPEG")
        return "converted_image.jpg"
    return file_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract-prescription', methods=['POST'])
def extract_prescription():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Allowed: jpg, jpeg, png, pdf"}), 400

    temp_filepath = f"temp_{file.filename}"
    file.save(temp_filepath)

    try:
        processed_file = pdf_to_image(temp_filepath)
        extracted_data = generate(processed_file)
    except Exception as e:
        extracted_data = {"error": f"Processing failed: {str(e)}"}
    
    os.remove(temp_filepath)
    try:
        os.remove("converted_image.jpg")
    except:
        pass

    return jsonify(extracted_data)

@app.route('/result', methods=['GET'])
def show_result():
    return render_template('result.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)