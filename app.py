from flask import Flask,jsonify
#jsonify() converts Python data to JSON response
import json

app = Flask(__name__)

@app.route('/')

def home():
    return "Hello Guy, lets begin with flask"

@app.route('/api')

#Read the data from backend file
def api():
    with open("data.json", "r") as file:
        data= json.load(file)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)