import cv2
import dlib
import csv
import os

def extract_landmarks(imgPath, csvPath, predictor_path="shape_predictor_68_face_landmarks.dat"):
    print(f"Loading face detector and predictor from {predictor_path}")
    # Load the detector
    detector = dlib.get_frontal_face_detector()
    # Load the predictor
    predictor = dlib.shape_predictor(predictor_path)

    print(f"Opening CSV file at {csvPath} to write landmarks")
    # Open a CSV file to write the landmarks
    with open(csvPath, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the header
        csvwriter.writerow(['image_name', 'face_id', 'point_id', 'x', 'y'])

        print(f"Reading image from {imgPath}")
        # Read the image
        img = cv2.imread(imgPath)
        if img is None:
            print(f"Error: Unable to read image at {imgPath}")
            return
        
        print("Converting image to grayscale")
        # Convert image into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        print("Detecting faces in the image")
        # Use detector to find the faces
        faces = detector(gray, 1)  # Increase the number of image pyramid layers to improve detection
        
        if len(faces) == 0:
            print("No faces detected")
        else:
            print(f"{len(faces)} face(s) detected")
            print(f"Landmarks have been saved to {csvPath}")

        face_id = 0
        for face in faces:
            print(f"Processing face {face_id}")
            # Create landmark object
            landmarks = predictor(gray, face)
            # Loop through all the points
            for n in range(0, 68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                # Write the landmarks to the CSV file
                csvwriter.writerow([os.path.basename(imgPath), face_id, n, x, y])
            face_id += 1
