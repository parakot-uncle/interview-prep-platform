from pyrebase import pyrebase

config = {
    "apiKey": "AIzaSyAhhZX5NgjypwjMO3vH_7Dakf5wH25arZc",
    "authDomain": "interview-prep-platform.firebaseapp.com",
    "projectId": "interview-prep-platform",
    "databaseURL": "https://interview-prep-platform-default-rtdb.firebaseio.com/",
    "storageBucket": "interview-prep-platform.appspot.com",
    "messagingSenderId": "563672832735",
    "appId": "1:563672832735:web:a0a59f027bddc24811e76a",
    "measurementId": "G-3EJFRWDBG6",
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()