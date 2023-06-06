from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os

# Import resume parsing libraries
from tika import parser
import docx2txt
import pdfplumber

# Import resume processing libraries
import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
file_path = "/result"
app = Flask(__name__)

# Configure the upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'docx', 'pdf'}

# Load spacy nlp model
nlp = spacy.load('en_core_web_sm')

def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        pages = pdf.pages
        text = ""
        for page in pages:
            text += page.extract_text()
        return text

def extract_information_from_resume(text):
    # Resume parsing logic goes here
    # Modify this function to extract the desired information from the resume text
    # For example, you can use regular expressions or spacy matching to extract names, email addresses, phone numbers, etc.
    # Return the extracted information as a dictionary
    
    extracted_info = {}
    # Extract name
    # Replace this with your own logic to extract the name from the resume text
    extracted_info['name'] = extract_name(text)
    
    # Extract email
    # Replace this with your own logic to extract the email from the resume text
    extracted_info['email'] = extract_email(text)
    
    # Extract phone number
    # Replace this with your own logic to extract the phone number from the resume text
    extracted_info['phone'] = extract_phone_number(text)
    
    return extracted_info

def extract_name(text):
    # Implement logic to extract name from resume text
    # Return the extracted name as a string
    return "John Doe"

def extract_email(text):
    # Implement logic to extract email from resume text
    # Return the extracted email as a string
    return "johndoe@example.com"

def extract_phone_number(text):
    # Implement logic to extract phone number from resume text
    # Return the extracted phone number as a string
    return "+1234567890"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_resume():
    # Check if the POST request has the file part
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file found'})

    file = request.files['resume']

    # Check if the file is allowed
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract text from the resume file
        text = ""
        if file_path.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        elif file_path.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)

        # Extract information from the resume text
        extracted_info = extract_information_from_resume(text)

        # Delete the uploaded file
        os.remove(file_path)

        return jsonify(extracted_info)

    return jsonify({'error': 'Invalid file'})

if __name__ == '__main__':
    app.run(debug=True)

