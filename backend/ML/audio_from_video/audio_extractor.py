import subprocess
import os
import sys
import uuid

def extract_audio(video_file):
    new_uuid = uuid.uuid4()

    audio_file_path = os.path.join(os.path.dirname(__file__), f"temp_{new_uuid}.wav")
    subprocess.call(["ffmpeg", "-y", "-i", video_file, audio_file_path], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    return audio_file_path
