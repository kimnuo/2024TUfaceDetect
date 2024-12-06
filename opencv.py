import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # TensorFlow 경고 억제

import cv2
import mediapipe as mp
from deepface import DeepFace

# Mediapipe FaceMesh 초기화
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

# OpenCV로 웹캠 열기
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("카메라에서 영상을 읽을 수 없습니다.")
        break

    # BGR 이미지를 RGB로 변환
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Mediapipe로 얼굴 특징 추출
    result = face_mesh.process(rgb_frame)

    # 감정 결과 초기화
    emotion = "No Emotion Detected"

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            for landmark in face_landmarks.landmark:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

        # DeepFace 감정 분석
        try:
            analysis = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
            # 반환값이 리스트일 경우 처리
            if isinstance(analysis, list):
                analysis = analysis[0]
            emotion = analysis["dominant_emotion"]
        except Exception as e:
            print(f"감정 분석 오류: {e}")

    # 감정을 화면에 표시
    cv2.putText(frame, f"Emotion: {emotion}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Real-time Emotion Detection", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
