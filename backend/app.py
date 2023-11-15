from flask import *
from flask_cors import CORS
from firebase import storage
from flask_pymongo import PyMongo
import urllib.parse
from dotenv import load_dotenv
import os
from bson import ObjectId, json_util
from datetime import datetime

import mediapipe as mp  # Import mediapipe
import cv2  # Import opencv

import csv
import os
import numpy as np

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

import pandas as pd
from sklearn.model_selection import train_test_split


from sklearn.metrics import accuracy_score  # Accuracy metrics
import pickle
from threading import Thread


mp_drawing = mp.solutions.drawing_utils  # Drawing helpers
mp_holistic = mp.solutions.holistic  # Mediapipe Solutions

cap = None
body_detections = []
def detect():
    global cap, body_detections
    with open("body_language.pkl", "rb") as f:
        model = pickle.load(f)

    cap = cv2.VideoCapture(0)
    # Initiate holistic model
    with mp_holistic.Holistic(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()

            # Recolor Feed
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make Detections
            results = holistic.process(image)
            # print(results.face_landmarks)

            # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks

            # Recolor image back to BGR for rendering
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # 1. Draw face landmarks
            mp_drawing.draw_landmarks(
                image,
                results.face_landmarks,
                mp_holistic.FACEMESH_TESSELATION,
                mp_drawing.DrawingSpec(
                    color=(80, 110, 10), thickness=1, circle_radius=1
                ),
                mp_drawing.DrawingSpec(
                    color=(80, 256, 121), thickness=1, circle_radius=1
                ),
            )

            # 2. Right hand
            mp_drawing.draw_landmarks(
                image,
                results.right_hand_landmarks,
                mp_holistic.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(
                    color=(80, 22, 10), thickness=2, circle_radius=4
                ),
                mp_drawing.DrawingSpec(
                    color=(80, 44, 121), thickness=2, circle_radius=2
                ),
            )

            # 3. Left Hand
            mp_drawing.draw_landmarks(
                image,
                results.left_hand_landmarks,
                mp_holistic.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(
                    color=(121, 22, 76), thickness=2, circle_radius=4
                ),
                mp_drawing.DrawingSpec(
                    color=(121, 44, 250), thickness=2, circle_radius=2
                ),
            )

            # 4. Pose Detections
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_holistic.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(
                    color=(245, 117, 66), thickness=2, circle_radius=4
                ),
                mp_drawing.DrawingSpec(
                    color=(245, 66, 230), thickness=2, circle_radius=2
                ),
            )
            # Export coordinates
            try:
                # Extract Pose landmarks
                pose = results.pose_landmarks.landmark
                pose_row = list(
                    np.array(
                        [
                            [landmark.x, landmark.y, landmark.z, landmark.visibility]
                            for landmark in pose
                        ]
                    ).flatten()
                )

                # Extract Face landmarks
                face = results.face_landmarks.landmark
                face_row = list(
                    np.array(
                        [
                            [landmark.x, landmark.y, landmark.z, landmark.visibility]
                            for landmark in face
                        ]
                    ).flatten()
                )

                # Concate rows
                row = pose_row + face_row

                X = pd.DataFrame([row])
                body_language_class = model.predict(X)[0]
                body_language_prob = model.predict_proba(X)[0]
                body_detections.append((body_language_class, body_language_prob))

                # Grab ear coords
                coords = tuple(
                    np.multiply(
                        np.array(
                            (
                                results.pose_landmarks.landmark[
                                    mp_holistic.PoseLandmark.LEFT_EAR
                                ].x,
                                results.pose_landmarks.landmark[
                                    mp_holistic.PoseLandmark.LEFT_EAR
                                ].y,
                            )
                        ),
                        [640, 480],
                    ).astype(int)
                )

                cv2.rectangle(
                    image,
                    (coords[0], coords[1] + 5),
                    (coords[0] + len(body_language_class) * 20, coords[1] - 30),
                    (245, 117, 16),
                    -1,
                )
                cv2.putText(
                    image,
                    body_language_class,
                    coords,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

                # Get status box
                cv2.rectangle(image, (0, 0), (250, 60), (245, 117, 16), -1)

                # Display Class
                cv2.putText(
                    image,
                    "CLASS",
                    (95, 12),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 0),
                    1,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    image,
                    body_language_class.split(" ")[0],
                    (90, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

                # Display Probability
                cv2.putText(
                    image,
                    "PROB",
                    (15, 12),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 0),
                    1,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    image,
                    str(round(body_language_prob[np.argmax(body_language_prob)], 2)),
                    (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

            except:
                pass

            cv2.imshow("Raw Webcam Feed", image)

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
        cap.release()
        cv2.destroyAllWindows()

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
            result_dict = json_util.loads(result_json)

            result_dict['detection'] = body_detections

            # Convert back to JSON string
            updated_result_json = json_util.dumps(result_dict)
            return updated_result_json

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
    thread = Thread(target = detect)
    thread.start()
    return {"message": "Recording started"}


if __name__ == "main":
    app.run(debug=True)
