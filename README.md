# Automatic Depression Detection Through Visual Inputs

This project aims to detect depression by analyzing emotional expressions in real-time video data using advanced machine learning techniques and a robust ETL pipeline. The system is designed to preprocess video inputs, extract relevant features, and detect emotions with co-relation with Beck Depression Inventory II score providing high accuracy, making it a valuable tool for mental health monitoring.

---

## Publication
https://ieeexplore.ieee.org/document/9210301

---

## Features
- **ETL Pipeline for Real-Time Video Processing**  
  Developed using Python for workflow orchestration, enabling efficient and scalable processing of video data with a 65% accuracy rate in emotion detection.

- **Image Preprocessing Pipeline**  
  Built with OpenCV, performing:
  - Frame separation
  - Brightness adjustment
  - Standardization to 48x48 grayscale images  
  Achieved 95% accuracy while effectively handling corrupted files and reducing noise.

- **Feature Extraction with CNNs**  
  Leveraged Convolutional Neural Networks (CNNs) and libraries like PyTorch, TensorFlow, Keras, and scikit-learn for advanced feature extraction. Optimized pipelines using vectorized operations in NumPy and cutting-edge preprocessing techniques, improving processing speed by 40%.

- **Interactive Web Application**  
  Designed a user-friendly interface with Flask, HTML, CSS, and JavaScript. The app allows users to upload video files for real-time emotion detection, seamlessly integrating backend processing and machine learning to deliver an engaging user experience.

---

## Technologies Used
- **Programming Languages**: Python, JavaScript, HTML, CSS  
- **Libraries and Frameworks**: OpenCV, Flask, TensorFlow, PyTorch, Keras, scikit-learn  
- **Web Development**: Flask, HTML, CSS, JavaScript  
- **Machine Learning**: CNNs for feature extraction and emotion detection

---

## Installation

### Prerequisites
- Python 3.8+
- Node.js (for JavaScript dependencies)
- Apache Airflow installed and configured
- Required Python libraries: pip install opencv-python flask tensorflow keras scikit-learn pytorch torchvision numpy

### Steps
1. Clone the repository:
 ```bash
 git clone https://github.com/AnaghaDhekne/Automatic-Depression-Detection.git
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the Flask app:
```bash
python app.py
```
4. Access the application at http://localhost:5000

---

## Usage
Upload a video file through the web application's interface.
The system will preprocess the video, extract features, and run the emotion detection model.
Results are displayed in real-time, highlighting detected emotions frame by frame.

---

## Results
Emotion Detection Accuracy: 65% on video data
Image Preprocessing Accuracy: 95% with noise and error reduction
Pipeline Optimization: 40% faster feature extraction and processing

---

## Contributing
Contributions are welcome! Please open an issue to discuss your ideas or submit a pull request.
