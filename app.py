from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

db = client["tutedude_assignment4"]
todo_collection = db["todo_items"]


@app.route("/")
def home():
    return "Assignment 4 - Git & GitHub"


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():

    item_name = request.form.get("itemName")
    item_description = request.form.get("itemDescription")

    if not item_name or not item_description:
        return jsonify({
            "error": "itemName and itemDescription are required"
        }), 400

    todo_item = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    result = todo_collection.insert_one(todo_item)

    return jsonify({
        "message": "To-Do item added successfully",
        "itemId": str(result.inserted_id),
        "itemName": item_name,
        "itemDescription": item_description
    }), 201


if __name__ == "__main__":
    app.run(debug=True)