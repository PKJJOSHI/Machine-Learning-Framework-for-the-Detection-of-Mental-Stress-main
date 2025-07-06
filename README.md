
<p align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHhxNjR4cWYzMHlkOG0zZmxvOHNpYjhhYjZ2M2pmbGNjZ3l6eDZmcCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/tIeCLkB8geYtW/giphy.gif" width="300" />
</p>

---

![Mental Stress Detection Banner](static/banner.png)
# 🧠 Machine Learning Framework for the Detection of Mental Stress

This project presents a real-time Face Emotion Recognition (FER) system designed to detect mental stress during digital learning sessions. Using a deep Convolutional Neural Network (CNN), the application analyzes facial expressions via webcam to determine stress levels and support mental well-being monitoring.

---

## 🚀 Features

- 🎥 Real-time facial emotion detection via webcam
- 🧠 CNN-based deep learning model (78% accuracy)
- 🌐 Flask-powered web application
- 📊 Interactive dashboard and emotional state visualization
- 🎨 Clean HTML/CSS user interface

---

## 📁 Project Structure

```
├── flask_app.py                  # Main Flask server script
├── model_weights_78.h5          # Pre-trained CNN model
├── requirements.txt             # Python dependencies
├── templates/
│   ├── index.html
│   ├── detection.html
│   └── dashboard.html
├── static/
│   └── styles.css
└── FER/
    └── open_cv/
        └── main.py              # Core face detection/emotion recognition logic
```

---

## 🧰 Technologies Used

- Python
- OpenCV
- Keras / TensorFlow
- Flask
- HTML, CSS (Frontend)

---

## ⚙️ How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/mental-stress-detector.git
   cd mental-stress-detector
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python flask_app.py
   ```

4. Open your browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

---

## 🎯 Model Accuracy

The emotion recognition model achieves **~78% accuracy** across multiple emotional states (happy, sad, angry, neutral, etc.).

---

## 📬 Contact

**Developer**: Prashant K. Joshi  
**LinkedIn**: [https://www.linkedin.com/in/prashantjoshi2220]  
**GitHub**: [https://github.com/PKJJOSHI)

---

## 📌 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
