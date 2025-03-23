# Prescription Extraction AI

This project is a Flask-based API that extracts relevant medical information from uploaded prescriptions (images or PDFs) using Google's Gemini AI. The API processes the prescription, extracts patient details, doctor details, and medication information, and returns structured JSON data.

## Features
- Supports image (`jpg`, `jpeg`, `png`) and PDF file formats.
- Converts PDF prescriptions to images for processing.
- Uses Google's Gemini AI for extracting structured medical information.
- Returns extracted data in JSON format.
- Simple API endpoint for integration into various platforms.

## Setup Guide

### Prerequisites
Ensure you have Python installed (version 3.8 or higher).

### Clone the Repository
```bash
git clone https://github.com/your-repo/prescription-extraction.git
cd prescription-extraction
```

### Install Dependencies
#### Option 1: Using `requirements.txt`
```bash
pip install -r requirements.txt
```

#### Option 2: Installing Manually
```bash
pip install dotenv google-genai flask pymupdf
```

### Set Up Environment Variables
To use the API, you need to obtain a Google Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).
Create a `.env` file in the root directory and add your Google Gemini API key:
```env
GEMINI_API_KEY="your_api_key_here"
```

## Running the API
```bash
python stand_alone.py
```
The server will start on `http://127.0.0.1:8000/`.

## API Endpoint
### `POST /extract-prescription/`
Uploads an image or PDF prescription for extraction.

#### Request
- `file` (multipart/form-data): The image or PDF file.

#### Example cURL Request (For Testing the API)
You can test the API using cURL with the following command:
```bash
curl -X POST "http://127.0.0.1:8000/extract-prescription/" -H "Content-Type: multipart/form-data" -F "file=@test_cases/check.jpg"
```
Alternatively, you can test it using Postman:
- Open Postman.
- Create a `POST` request to `http://127.0.0.1:8000/extract-prescription/`.
- Select `form-data`, add a `file` key, and upload an image or PDF.
- Click `Send` and check the JSON response.

#### Response (Example JSON Output)
```json
{
    "Patient's full name": "John Doe",
    "Patient's age": "45y",
    "Patient's gender": "Male",
    "Doctor's full name": "Dr. Jane Smith",
    "Doctor's license number": "ABC123456",
    "Prescription date": "2023-04-01",
    "Medications": [
        {
            "Medication name": "Amoxicillin",
            "Dosage": "500 mg",
            "Frequency": "Twice a day (TD)",
            "Duration": "7 days",
            "Medicine Description": "Zincowil Tablet is a nutritional supplement that is used to treat deficiencies of zinc in the body. It is often used to boost the immune system and for overall growth and well-being.",
            "Medicine Usage": "It is used to treat zinc deficiency, strengthen the immune system, and support overall health.",
            "Medicine Side effects": "Generally considered safe, but high doses of zinc can cause side effects like nausea, vomiting, diarrhea, and metallic taste in the mouth.",
        }
    ],
    "Additional notes": {
        "General Advice": [
            "Take medication after food.",
            "Avoid sugary foods.",
            "Monitor blood sugar levels daily."
        ],
        "Duration": "(2)d: Two days",
        "Complaints of (c/o)": [
            "Dry cough",
            "Chest pain"
        ],
        "Contact Information": "For concerns, message on WhatsApp: 4587632118.",
        "Disclaimer": "Note: Not for Medico legal purpose"
    }
}
```

## Accessing the API Using Other Programming Languages
You can integrate and access the API using:
- **Python (Django, Flask)**
- **MERN Stack (MongoDB, Express, React, Node.js)**
- **PHP**
- **Mobile Apps (Android, iOS)**
- **Any other language that supports API requests**

## Notes
- Ensure your Google API key is valid.
- If using a PDF, only the first page will be processed.
- Invalid or unreadable prescriptions will return `"not a prescription"`.

## Future Enhancements
Exciting updates are on the way! Soon, a Flask-based web app will be released alongside this standalone API. This web app will provide a user-friendly interface where users can easily upload prescription images and instantly receive extracted results.

Stay tuned for more updates!

