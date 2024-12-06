import cv2
import os
import shutil

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Define the source and destination directories
source_dir = 'C:/Users/kevin/Downloads/Selected1129/angry'
destination_dir = 'C:/Users/kevin/OneDrive - 한국공학대학교/tuk2024/인공지능 2-2/팀플/faceDetect/data/angry'

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Iterate through all files in the source directory
for filename in os.listdir(source_dir):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Read the image
        img_path = os.path.join(source_dir, filename)
        img = cv2.imread(img_path)
        
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # If faces are detected, move the image to the destination directory
        if len(faces) > 0:
            shutil.move(img_path, os.path.join(destination_dir, filename))

print("Face detection and image moving completed.")