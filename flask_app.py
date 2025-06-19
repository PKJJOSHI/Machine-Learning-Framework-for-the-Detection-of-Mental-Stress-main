from flask import Flask, render_template, Response, jsonify, request
from flask import Flask, render_template, Response, jsonify, request

from PIL import Image

import matplotlib.pyplot as plt
import io
import base64

import cv2
import numpy as np
from keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

app = Flask(__name__)

# Load model
classifier = load_model('model_78.h5')
classifier.load_weights("model_weights_78.h5")

# Define the emotions
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise', 'Stress']

# Load face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def calculate_stress_level(emotion):
    stress_levels = {
        'Angry': 80,
        'Disgust': 60,
        'Fear': 70,
        'Happy': 10,
        'Neutral': 30,
        'Sad': 50,
        'Surprise': 40
    }
    return stress_levels.get(emotion, 0)

def create_plot(stress_levels, emotions, emotion_counts):
    plt.figure(figsize=(10, 5))  # Stress Level Plot
    plt.plot(stress_levels, label='Stress Level', color='blue')
    plt.xlabel('Time')
    plt.ylabel('Stress Level (%)')
    plt.title('Live Stress Level')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    
    # Save the plot to a BytesIO object and encode it to base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def create_plot_emotions(emotion_counts):
    plt.figure(figsize=(10, 5))  # Emotion Counts Plot
    plt.bar(emotion_counts.keys(), emotion_counts.values(), color='orange')
    plt.xlabel('Emotions')
    plt.ylabel('Counts')
    plt.title('Facial Emotion Counts')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot to a BytesIO object and encode it to base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

stress_levels = []
emotions = []
emotion_counts = {label: 0 for label in emotion_labels}  # Initialize emotion counts

def generate_frames():
    global emotions  # Declare emotions as global to modify it

    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(img_gray, scaleFactor=1.3, minNeighbors=5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                roi_gray = img_gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
                if np.sum([roi_gray]) != 0:
                    roi = roi_gray.astype('float') / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)
                    prediction = classifier.predict(roi)[0]
                    maxindex = int(np.argmax(prediction))
                    finalout = emotion_labels[maxindex]
                    stress_level = calculate_stress_level(finalout)
                    stress_levels.append(stress_level)
                    emotions.append(finalout)
                    stress_percentage = f"Stress Level: {stress_level}%"
                    emotion_counts[finalout] += 1  # Increment the count for the detected emotion

                    label_position = (x, y - 10)
                    cv2.putText(frame, stress_percentage, (x, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    cv2.putText(frame, finalout, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/dashboard')
def dashboard():
    # Create the plots
    plot_url_stress = create_plot(stress_levels, emotions, emotion_counts)  # Stress Level Plot
    plot_url_emotions = create_plot_emotions(emotion_counts)  # Emotion Counts Plot

    return render_template('dashboard.html', plot_url_stress=plot_url_stress, plot_url_emotions=plot_url_emotions)  # Render the dashboard HTML template

@app.route('/')
def index():
    return render_template('index.html')  # Render the updated HTML template

@app.route('/detection')
def detection():
    return render_template('detection.html')  # Render the detection HTML template



@app.route('/video_feed')


def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')  # Serve the video feed

if __name__ == '__main__':
    app.run(debug=True)
