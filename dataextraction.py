import os
import shutil

def clean_and_copy_files(base_path, target_path):
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    emotions = {
        'E01': 'neutral',
        'E02': 'happy',
        'E03': 'angry'
    }

    for emotion in emotions.values():
        emotion_path = os.path.join(target_path, emotion)
        if not os.path.exists(emotion_path):
            os.makedirs(emotion_path)
    
    cnt = 0 
    for top_folder in os.listdir(base_path):
        top_folder_path = os.path.join(base_path, top_folder)
        if os.path.isdir(top_folder_path) and top_folder.isdigit():
            for s_folder in range(1, 7):
                s_folder_path = os.path.join(top_folder_path, f's{s_folder:03d}')
                for l_folder in range(1, 5):
                    l_folder_path = os.path.join(s_folder_path, f'L{l_folder}')
                    for e_folder in range(1, 4):
                        e_folder_path = os.path.join(l_folder_path, f'E{e_folder:02d}')
                        emotion = emotions.get(f'E{e_folder:02d}')
                        if emotion:
                            emotion_path = os.path.join(target_path, emotion)
                            for c_file in range(1, 9):
                                c_file_path = os.path.join(e_folder_path, f'C{c_file}.jpg')
                                if os.path.exists(c_file_path):
                                    if 6 <= c_file <= 8:
                                        new_file_name = f'C{cnt:04d}.jpg'
                                        new_file_path = os.path.join(emotion_path, new_file_name)
                                        shutil.copy2(c_file_path, new_file_path)
                                        cnt += 1
                                else:
                                    print(f"File not found: {c_file_path}")

base_path = r'C:/Users/kevin/Downloads/Middle_Resolution'
target_path = r'C:/Users/kevin/OneDrive - 한국공학대학교/tuk2024/인공지능 2-2/팀플/faceDetect/fdata'
clean_and_copy_files(base_path, target_path)