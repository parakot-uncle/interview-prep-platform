from flask import *
from flask_cors import CORS
from firebase import storage

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["POST"])
def base():
  files = request.files
  video = files["video"]
  temp_file_path = 'temp_video.webm'

  video_path = f"/temp/{temp_file_path}"
  storage.child(video_path).put(video)

  return storage.child(video_path).get_url(None)

if __name__ == "main":
  app.run(debug=True)


