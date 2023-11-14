from flask import *
from flask_cors import CORS
from firebase import storage
from flask_pymongo import PyMongo
import urllib.parse
from dotenv import load_dotenv
import os
from bson import ObjectId, json_util
from datetime import datetime

load_dotenv()

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
database_name = os.getenv("MONGO_DB_NAME")

app = Flask(__name__)
CORS(app)
app.config[
    "MONGO_URI"
] = f"mongodb+srv://{username}:{password}@cluster0.fyggxfu.mongodb.net/{database_name}?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = mongo.db


@app.route("/mock-interview-attempts", methods=["GET", "POST"])
def attempt():
    if request.method == "POST":
        files = request.files
        form_data = request.form

        video = files["video"]
        date = datetime.now()
        user_id = form_data["user"]
        question = form_data["question"]

        video_path = f"/mock-interviews/{user_id}/{date}.webm"
        storage.child(video_path).put(video)
        video_url = storage.child(video_path).get_url(None)

        attempt = {
            "user": ObjectId(user_id),
            "video": video_url,
            "date": date,
            "question": question,
        }

        res = db["mock-interview-attempt"].insert_one(attempt)

        if res.acknowledged:
            inserted_attempt = mongo.db["mock-interview-attempt"].find_one(
                {"_id": res.inserted_id}
            )
            result_json = json_util.dumps(inserted_attempt)
            return result_json

        return res

    if request.method == "GET":
        user_id = request.args.get("user_id")
        question = request.args.get("question")

        query = {"$and": [{"user": ObjectId(user_id)}, {"question": question}]}
        attempts_cursor = db["mock-interview-attempt"].find(query).sort("date", -1)
        
        attempts_list = list(attempts_cursor)
        result_json = json_util.dumps(attempts_list)
        return result_json


if __name__ == "main":
    app.run(debug=True)
