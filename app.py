from flask import Flask, request, jsonify, render_template
from paser import ResumeParser
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')

        parser = ResumeParser(file)
        data = parser.parse_resume()

    
        return jsonify(data)
       
if __name__ == '__main__':
    app.run(debug=True,port=5000,host="0.0.0.0")
