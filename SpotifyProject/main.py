from flask import Flask, render_template, Response
from FaceRecognition import face_rec
import time

app = Flask(__name__)

rec = face_rec()

@app.route('/')
def index():
    return render_template("index.html")
    
def gen(FaceRecognition):
    
    while True:
        video_frame = rec.get_frames()
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + video_frame + b'\r\n\r\n')
        
@app.route('/video_feed')
def video_feed():
    return Response(gen(face_rec),
    mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/start_recognition')
def start_recognition():
    verified = rec.recognition()
    
    if verified:
        return render_template("success.html")
    else:
        return render_template("failed.html")
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True)
