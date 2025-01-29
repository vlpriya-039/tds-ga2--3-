from flask import Flask, request, jsonify
import pandas as pd
from io import StringIO
import os

app = Flask(__name__)

# Load student marks data (replace with your actual loading method)
# Assuming the data is in a CSV format as you described.
# Since you mentioned you have the data, I'll assume you know how to load it.
# I'll show a basic example.
csv_data = """
Name,Math,Science,English
Alice,85,92,78
Bob,76,88,95
Charlie,90,80,85
... (rest of your data)
"""
df = pd.read_csv(StringIO(csv_data))

# Enable CORS for all origins (adjust as needed for production)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')  # Allow from any origin
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response

@app.route('/api')
def get_marks():
    names = request.args.getlist('name')  # Get a list of names
    marks = []

    for name in names:
        # Find the row corresponding to the name (case-insensitive)
        student_data = df[df['Name'].str.lower() == name.lower()]
        if not student_data.empty:  # Check if the student exists
            # Assuming you want the math marks for now. You can change this.
            mark = student_data['Math'].values[0]
            marks.append(mark)
        else:
            marks.append(None)  # Add None if student not found

    return jsonify({"marks": marks})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) #For Vercel