from flask import *
from flask_cors import CORS
from firebase import storage
from flask_pymongo import PyMongo
import urllib.parse
from dotenv import load_dotenv
import os
from bson import ObjectId, json_util
from datetime import datetime

from ML.BodyDetect.Body_Language_Decoder import detect

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

        body_detections, output_video = detect(video_url)
        print(body_detections)

        video_path = f"/mock-interviews/{user_id}/{date}_detected.webm"
        storage.child(video_path).put(output_video)
        video_url = storage.child(video_path).get_url(None)

        os.remove(output_video)

        body_detection_uploads = []

        for detection in body_detections:
            print(detection)
            image_path = (
                f"/mock-interviews/{user_id}/{date}_detected_{detection['image']}"
            )
            storage.child(image_path).put(detection["image"])
            image_url = storage.child(image_path).get_url(None)

            upload = dict()
            upload["detection"] = detection["detection"]
            upload["image"] = image_url

            body_detection_uploads.append(upload)

            os.remove(detection["image"])

        if res.acknowledged:


            updated_attempt = {
                "body_detections": body_detection_uploads,
                "detected_video": video_url,
            }
            update_query = {"$set": updated_attempt}

            result = db["mock-interview-attempt"].update_one(
                {"_id": res.inserted_id}, update_query
            )

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


@app.route("/start-recording", methods=["POST"])
def start_recording():
    # thread = Thread(target = detect)
    # thread.start()
    # detect()
    return {"message": "Recording started"}


if __name__ == "main":
    app.run(debug=True)
