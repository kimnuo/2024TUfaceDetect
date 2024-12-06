import cv2
import dlib
import csv
import os

# Load the detector
detector = dlib.get_frontal_face_detector()
# Load the predictor
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Define the source directory
source_dir = 'fdata/neutral'
# Define the output CSV file path
csv_file_path = 'output/neutral.csv'

# Create the output directory if it doesn't exist
output_dir = os.path.dirname(csv_file_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Open a CSV file to write the landmarks
with open(csv_file_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header
    csvwriter.writerow(['image_name', 'face_id', 'point_id', 'x', 'y'])

    # Iterate through all files in the source directory
    for filename in os.listdir(source_dir):
        if filename.endswith('.jpg'):
            print(f"Processing file: {filename}")
            # Read the image
            img_path = os.path.join(source_dir, filename)
            img = cv2.imread(img_path)
            
            # Convert image into grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Use detector to find the faces
            faces = detector(gray)
            
            face_id = 0
            for face in faces:
                # Create landmark object
                landmarks = predictor(gray, face)
                # Loop through all the points
                for n in range(0, 68):
                    x = landmarks.part(n).x
                    y = landmarks.part(n).y
                    # Write the landmarks to the CSV file
                    csvwriter.writerow([filename, face_id, n, x, y])
                face_id += 1

print(f"Landmarks have been saved to {csv_file_path}")