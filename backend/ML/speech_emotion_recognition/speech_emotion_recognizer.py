from transformers import pipeline
import os


model_path = os.path.join(os.path.dirname(__file__), "model")
pipe = pipeline("audio-classification", model_path)
# pipe = pipeline("audio-classification", model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition")
print(
    pipe(
        "https://firebasestorage.googleapis.com/v0/b/interview-prep-platform.appspot.com/o/mock-interviews%2F6553a5289f33c7101f5ee3b4%2F655640d8b8cc0a410363e631%2F2023-11-17%2014%3A54%3A22.626616.webm?alt=media"
    )
)
