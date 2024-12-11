import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Conv1D, Dropout, BatchNormalization, GlobalAveragePooling1D
from tensorflow.keras.callbacks import Callback, ReduceLROnPlateau
from model_analyzer import NEpochCallback, NBatchCallback
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score, precision_score, recall_score

# 이미지 별 x, y 좌표 추출
def extract_coordinates(dataframe):
    coordinates = {}
    for image_name in dataframe['image_name'].unique():
        # 해당 이미지의 데이터 필터링
        image_data = dataframe[dataframe['image_name'] == image_name]
        # x, y 좌표 배열 생성
        x_coords = image_data['x'].tolist()
        y_coords = image_data['y'].tolist()
        # 딕셔너리에 저장
        coordinates[image_name] = {'x': x_coords, 'y': y_coords}
    return coordinates



neutral_df = pd.read_csv("../output/neutral.csv")
angry_df = pd.read_csv("../output/angry.csv")
happy_df = pd.read_csv("../output/happy.csv")
neutral_df['label'] = 0
happy_df['label'] = 1
angry_df['label'] = 2

face_metadata_df = pd.concat([neutral_df, angry_df, happy_df], ignore_index=True)
face_metadata_df = face_metadata_df.sort_values(by="image_name")

face_metadata_df.head(5)

x_face_metadata_df = face_metadata_df.drop('label', axis=1)
y_face_metadata_df = face_metadata_df[['image_name', 'label']]

x_face_metadata_df.head(5)

y_face_metadata_df.head(5)

def convert_to_X_train(target_df: pd.DataFrame):
    result = list()
    image_names = (target_df["image_name"]).unique()

    for image_name in image_names:
        points = target_df[target_df["image_name"] == image_name][["x", "y"]].values
        result.append(points)
    
    return np.array(result)
    
x_train_data = convert_to_X_train(x_face_metadata_df)

def convert_to_Y_train(target_df: pd.DataFrame):
    result = target_df.drop_duplicates('image_name').copy()
    result['neutral'] = result['label'].map({ 0: 1, 1: 0, 2: 0})
    result['happy'] = result['label'].map({ 0: 0, 1: 1, 2: 0 })
    result['angry'] = result['label'].map({ 0: 0, 1: 0, 2: 1 })                                           
    
    return np.array(result.drop(['image_name', 'label'], axis=1))

y_train_data = convert_to_Y_train(y_face_metadata_df)

X_train, X_test, Y_train, Y_test = train_test_split(x_train_data,
                                                    y_train_data,
                                                    test_size=0.2,
                                                    random_state=11)

print(X_train.shape[0])
print(Y_train.shape[0])

model = Sequential([
    Conv1D(64, kernel_size=3, activation='relu', input_shape=(68, 2)),
    BatchNormalization(),  # 모델 안정화
    Dense(32 , activation='relu'),
    Dense(32 , activation='relu'),
    Dense(64 , activation='relu'),
    Dense(128, activation='relu'), 
    Dense(256, activation='relu'), Dropout(0.5),
    Dense(256, activation='relu'), Dropout(0.5),  
    Dense(128, activation='relu'),
    Dense(64 , activation='relu'),
    Dense(32 , activation='relu'),
    Dense(32 , activation='relu'),
    
    GlobalAveragePooling1D(),
    Dense(3, activation='softmax') # 출력층
])



batch_callback = NBatchCallback(n=10)
epoch_callback = NEpochCallback(n= 2, filepath="./weights/")

reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6)
model.compile(optimizer='nadam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(X_train, Y_train, epochs=10, batch_size=128, callbacks=[batch_callback, epoch_callback])


y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = np.argmax(Y_test, axis=1)

accuracy = accuracy_score(y_true, y_pred_classes)
precision = precision_score(y_true, y_pred_classes, average='weighted')
recall = recall_score(y_true, y_pred_classes, average='weighted')
f1 = f1_score(y_true, y_pred_classes, average='weighted')

print(f"Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")