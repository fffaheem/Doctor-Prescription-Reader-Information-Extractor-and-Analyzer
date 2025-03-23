import base64
import os
from google import genai
from google.genai import types
import json
from dotenv import load_dotenv


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def generate(filepath):

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    model = "gemini-2.0-pro-exp-02-05"
    # model = "gemini-2.0-flash"
    with open(filepath, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_bytes(
                    mime_type="""image/jpeg""",
                    data=base64.b64decode(encoded_image),
                ),
                types.Part.from_text(text="""You are an expert medical transcriptionist specializing in deciphering and accurately transcribing handwritten medical prescriptions. Your role is to meticulously analyze the provided prescription images and extract all relevant information with the highest degree of precision.

    Here are some examples of the expected output format:

    Example 1:
    Patient's full name: John Doe
    Patient's age: 45 /45y
    Patient's gender: M/Male
    Doctor's full name: Dr. Jane Smith
    Doctor's license number: ABC123456
    Prescription date: 2023-04-01
    Medications:
    - Medication name: Amoxicillin
      Dosage: 500 mg
      Frequency: (TD) Twice a day
      Duration: 7 days
      Medicine Description: aasdasd
      Medicine Usage: ldfm
      Medicine Side effects: jhjhsdf
    - Medication name: Ibuprofen
      Dosage: 200 mg
      Frequency: Every 4 hours as needed
      Duration: 5 days
      Medicine Description: aasdasd
      Medicine Usage: ldfm
      Medicine Side effects: jhjhsdf
    Additional notes:

      -General Advice:
          Take medication after food
          Avoid Sugary foods
          Monitor blood sugar levels daily

      -Duration:
          (2)d: Two days

      -(c/o) complaints of:
          Dry cough
          Chest pain

      -Contact Information:
          For concerns, message on WhatsApp: 4587632118.

      -Disclaimer:
          *Note: Not for Medico legal purpose

    Example 2:
    Patient's full name: Jane Roe
    Patient's age: 60/60y
    Patient's gender: F/Female
    Doctor's full name: Dr. John Doe
    Doctor's license number: XYZ654321
    Prescription date: 2023-05-10
    Medications:
    - Medication name: Metformin
      Dosage: 850 mg
      Frequency: (OD) Once a day
      Duration: 30 days
      Medicine Description: aasdasd
      Medicine Usage: ldfm
      Medicine Side effects: jhjhsdf
    Additional notes:

      -General Advice:
          Plenty of oral fluids.
          "Danger signs" explained.
          Steam + Gargle

      -Duration:
          (3)d: Three days

      -(c/o) complaints of:
          Dry cough
          Rhinitis
          Chest pain

      -Contact Information:
          For concerns, message on WhatsApp: 8445537118.

      -Disclaimer:
          *Note: Not for Medico legal purpose

    Your job is to extract and accurately transcribe the following details from the provided prescription images:
    1. Patient's full name
    2. Patient's age (handle different formats like \"42y\", \"42yrs\", \"42\", \"42 years\")
    3. Patient's gender
    4. Doctor's full name
    5. Doctor's license number
    6. Prescription date (in YYYY-MM-DD format)
    7. List of medications including:
       - Medication name
       - Dosage
       - Frequency
       - Duration
    8. Additional notes or instructions. Provide detailed and enhanced notes using bullet points. Organize the notes in clear bullet points for better readability.
        - Provide detailed and enhanced notes using bullet points.
        - If there are headings or categories within the notes, ensure the bullet points are organized under those headings.
        - Use clear and concise language to enhance readability.
        - Ensure the notes are structured in a way that makes them easy to follow and understand.

        - make sure it looks like this 
            Additional notes:

              General Advice:
                  Plenty of oral fluids.
                  "Danger signs" explained.
                  Steam + Gargle

              Duration:
                  (3)d: Three days

              (c/o) complaints of:
                  Dry cough
                  Rhinitis
                  Chest pain

              Contact Information:
                  For concerns, message on WhatsApp: 8445537118.

              Disclaimer:
                  Note: Not for Medico legal purpose

    Important Instructions:
    - Before extracting information, enhance the image for better readability if needed. Use techniques such as adjusting brightness, contrast, or applying filters to improve clarity.
    - Ensure that each extracted field is accurate and clear. If any information is not legible or missing, indicate it as 'Not available'.
    - Do not guess or infer any information that is not clearly legible.
    - Do not make assumptions or guesses about missing information.
    - Pay close attention to details like medication names, dosages, and frequencies.
    - Before you write the output of the medicine search the internet for the existing medicine name to make easier for user to know exactly what the medications are. mostly the medicine will be for indian audience.
    - Always mention both the short form and full form such as OD as well as Once a day, c/o and complaints of and similarly for all others. always include full form of everything
    - Also, tell about the medicine that you are precisibing and what are it's uses and side effects so that the patient can be vary when taking them
    - Medicine description, uses and side effects should always be a text not another list or json
    - If Additional information is not there still display it if sub heading of addition information is not there still display it with information not available and do not create more subheadings
    - all additional subheading should contain a list of text
    - this is needed for a website so format need to be strictly followed
    - give JSON of it
    - very important instruction if it's not a presription just return \"not a prescription\" 
    - disclamer is going to be the same always Note: Not for Medico legal purpose"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=64,
        max_output_tokens=8192,
        # response_mime_type="text/plain",
        response_mime_type="application/json",
    )

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response_text += chunk.text
        # print(chunk.text, end="")
    data = json.loads(response_text)  
    return data





# d = generate("./test_cases/check.jpg")
# print(d)
