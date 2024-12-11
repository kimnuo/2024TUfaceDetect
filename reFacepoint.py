import cv2
import csv
import os
import numpy as np

# Define the source CSV file and output directory
csv_file = 'static\\facedata\\face.csv'
output_dir = 'static'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Dictionary to store landmarks for each image
landmarks_dict = {}

# Read the CSV file
with open(csv_file, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header
    for row in csvreader:
        image_name, face_id, point_id, x, y = row
        if image_name not in landmarks_dict:
            landmarks_dict[image_name] = []
        landmarks_dict[image_name].append((int(x), int(y)))

# Iterate through the landmarks dictionary and create images
for image_name, landmarks in landmarks_dict.items():
    # Create a blank image
    img = 255 * np.ones(shape=[500, 500, 3], dtype=np.uint8)
    
    # Draw the landmarks on the image
    for (x, y) in landmarks:
        cv2.circle(img, (x, y), 2, (0, 0, 255), -1)
    
    # Save the image
    output_path = os.path.join(output_dir, image_name)
    cv2.imwrite(output_path, img)

print("Images have been created and saved to the output directory.")