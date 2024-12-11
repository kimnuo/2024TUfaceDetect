import os
from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
import requests
import facepoint as fp  # 특징점 추출 모듈
import facedetect as fd  # 얼굴 인식 모듈

app = Flask(__name__)

UPLOAD_FOLDER = 'static/facedata'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# uploads 폴더가 존재하지 않으면 생성하고 권한 설정
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'])
        os.chmod(app.config['UPLOAD_FOLDER'], 0o777)  # 모든 사용자에게 읽기/쓰기 권한 부여
    except Exception as e:
        print(f"Error creating directory: {e}")
        
def facial_expression_extraction():  # 표정 추출 모델 연결
    url = "http://192.168.20.1:6000/generate"
    try:
        data = {
            "user_input": np.genfromtxt('static/facedata/face.csv', delimiter=',').tolist()
        }
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print(f"Error during facial expression extraction: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload-face', methods=['POST'])
def upload_face():
    try:
        faceP = "static/facedata/faceUp.jpg"
        csvP = "static/facedata/face.csv"
        
        if(fd.detect_faces_in_image(faceP)):
            print("Face detected")
            fp.extract_landmarks(faceP, csvP)
        
        return jsonify({'success': 'Face captured successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/capture-face', methods=['POST'])
def capture_face():
    try:
        data = request.get_json()
        img_data = data['image']
        img_data = img_data.split(',')[1]  # 데이터 URL에서 base64 부분만 추출
        img_data = base64.b64decode(img_data)

        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({'error': 'Failed to decode image'}), 400
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'face.jpg')
        cv2.imwrite(filename, img)
        print("Image saved to", filename)
        
        faceP = "static/facedata/face.jpg"
        csvP = "static/facedata/face.csv"
        
        if(fd.detect_faces_in_image(faceP)):
            print("Face detected")
            fp.extract_landmarks(faceP, csvP)
        
        return jsonify({'success': 'Face captured successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/expBtn', methods=['POST'])
def exp_btn():
    #facial_expression_extraction() # 표정 추출
    return jsonify('인식 완료')

if __name__ == '__main__':
    app.run(debug=True,port=5600)