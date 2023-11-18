from transformers import pipeline
import os

def recognize(audio_file):
    model_path = os.path.join(os.path.dirname(__file__), "model")
    pipe = pipeline("audio-classification", model_path)

    emotions = pipe(audio_file)
    return emotions[0]["label"]
