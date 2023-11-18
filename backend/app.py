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
from threading import Thread
from ML.audio_from_video.audio_extractor import extract_audio
from ML.speech_to_text.speech_to_text_converter import convert
from ML.answer_comparison.compare_answer import short
from ML.speech_emotion_recognition.speech_emotion_recognizer import recognize
from ML.flag_words_detection.flag_words_detector import detect_flag_words

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


def process_body_detection(doc_id, user_id, question, date, video_url):
    body_detections, output_video = detect(video_url)
    print(body_detections)

    video_path = f"/mock-interviews/{user_id}/{question}/{date}_detected.webm"
    storage.child(video_path).put(output_video)
    video_url = storage.child(video_path).get_url(None)

    os.remove(output_video)

    body_detection_uploads = []

    for detection in body_detections:
        print(detection)
        image_path = f"/mock-interviews/{user_id}/{question}/{date}_detected_{detection['image']}"
        storage.child(image_path).put(detection["image"])
        image_url = storage.child(image_path).get_url(None)

        upload = dict()
        upload["detection"] = detection["detection"]
        upload["image"] = image_url

        body_detection_uploads.append(upload)

        os.remove(detection["image"])

    updated_attempt = {
        "body_detections": body_detection_uploads,
        "detected_video": video_url,
    }
    update_query = {"$set": updated_attempt}

    result = db["mock-interview-attempt"].update_one({"_id": doc_id}, update_query)


def process_audio(doc_id, video_url, question_id, category):
    audio_path = extract_audio(video_url)
    user_answer = convert(audio_path)
    emotion_detected = recognize(audio_path)


    collection_name = f"{category}-mock-interview-questions"
    question = db[collection_name].find_one({"_id": ObjectId(question_id)})

    updated_attempt = {
        "user_answer": user_answer,
        "emotion_detected_from_audio": emotion_detected,
    }

    if category == "hr":
        flag_words_similarity = detect_flag_words(user_answer, question["flag_words"])
        updated_attempt["flag_words_similarity_score"] = flag_words_similarity
    else:
        similarity_score = short(user_answer, question["answer"])
        updated_attempt["answer_similarity_score"] = similarity_score           

    os.remove(audio_path)

    update_query = {"$set": updated_attempt}

    result = db["mock-interview-attempt"].update_one({"_id": doc_id}, update_query)


@app.route("/mock-interview-attempts", methods=["GET", "POST"])
def mock_interview_attempts():
    if request.method == "POST":
        files = request.files
        form_data = request.form

        video = files["video"]
        date = datetime.now()
        user_id = form_data["user"]
        question = form_data["question"]
        category = form_data["question_category"]

        video_path = f"/mock-interviews/{user_id}/{question}/{date}.webm"
        storage.child(video_path).put(video)
        video_url = storage.child(video_path).get_url(None)

        attempt = {
            "user": ObjectId(user_id),
            "video": video_url,
            "date": date,
            "question": ObjectId(question),
        }

        res = db["mock-interview-attempt"].insert_one(attempt)

        body_detection_thread = Thread(
            target=process_body_detection,
            args=(res.inserted_id, user_id, question, date, video_url),
        )
        body_detection_thread.start()

        audio_processing_thread = Thread(
            target=process_audio, args=(res.inserted_id, video_url, question, category)
        )
        audio_processing_thread.start()

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

        query = {
            "$and": [{"user": ObjectId(user_id)}, {"question": ObjectId(question)}]
        }
        attempts_cursor = db["mock-interview-attempt"].find(query).sort("date", -1)

        attempts_list = list(attempts_cursor)
        result_json = json_util.dumps(attempts_list)
        return result_json


@app.route("/start-recording", methods=["POST"])
def start_recording():
    return {"message": "Recording started"}


@app.route("/mock-interview-questions/<string:category>", methods=["GET"])
def mock_interview_questions(category):
    collection_name = f"{category}-mock-interview-questions"
    questions = db[collection_name].find()

    result_json = json_util.dumps(questions)
    return result_json


if __name__ == "main":
    app.run(debug=True)
