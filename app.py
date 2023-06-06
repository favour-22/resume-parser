from flask import Flask, render_template, request, jsonify
from Resume import ResumeParser

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded file from the request
    file = request.files['resume']

    # Create a ResumeParser object and parse the resume
    parser = ResumeParser(file)
    data = parser.parse_resume()

    # Convert the extracted information into a JSON response
    response = jsonify(data)
    response.status_code = 200
    return response

if __name__ == '__main__':
    app.run(debug=True)
