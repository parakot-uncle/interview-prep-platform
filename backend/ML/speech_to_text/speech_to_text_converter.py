import speech_recognition as sr


# Initialize recognizer class (for recognizing the speech)
def convert(fileName):
    r = sr.Recognizer()
    # Reading Microphone as source
    # listening the speech and store in audio_text variable
    with sr.AudioFile(fileName) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        return text
