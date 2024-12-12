import cv2
import numpy as np
import os

def extract_rgb_matrix(image_path):
    # 이미지 읽기
    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError("이미지를 읽을 수 없습니다. 경로를 확인하세요.")
    
    # 이미지의 크기 가져오기
    height, width, _ = image.shape
    
    # n*n*3 행렬 생성
    rgb_matrix = np.zeros((height, width, 3), dtype=np.uint8)
    
    # 각 픽셀의 RGB 값 추출
    for i in range(height):
        for j in range(width):
            rgb_matrix[i, j] = image[i, j]
    
    return rgb_matrix

def save_rgb_matrix_to_file(rgb_matrix, file_path):
    np.save(file_path, rgb_matrix)

def process_all_images_in_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(directory_path, filename)
            output_file_path = os.path.join(directory_path, f"{os.path.splitext(filename)[0]}.npy")
            
            if os.path.exists(output_file_path):
                print(f"Skipping {filename}, .npy file already exists.")
                continue
            
            rgb_matrix = extract_rgb_matrix(image_path)
            save_rgb_matrix_to_file(rgb_matrix, output_file_path)
            print(f"RGB matrix saved to {output_file_path}")

# 디렉토리 경로 설정
directory_path = 'C:\\coding\\2024TUfaceDetect\\fdata\\neutralProc'
process_all_images_in_directory(directory_path)
