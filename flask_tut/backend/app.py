from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

client = pymongo.MongoClient(MONGO_URL)
db = client.test
collection = db["flask_tut"]

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend running successfully"

@app.route("/submit", methods=["POST"])
def submit():
    try:
        form_data = dict(request.json)

        if not form_data.get("name") or not form_data.get("password"):
            return jsonify({
                "status": "error",
                "message": "All fields are required"
            }), 400

        collection.insert_one(form_data)

        return jsonify({
            "status": "success",
            "message": "Data submitted successfully"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/view")
def view():
    data = list(collection.find())

    for item in data:
        item["_id"] = str(item["_id"])

    return jsonify({"data": data})


@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    try:
        data = request.json

        item = {
            "itemName": data.get("itemName"),
            "itemDescription": data.get("itemDescription")
        }

        collection.insert_one(item)

        return jsonify({
            "status": "success",
            "message": "To-Do item stored"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9000))
    app.run(host="0.0.0.0", port=port, debug=True)