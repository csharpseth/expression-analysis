import os
import cv2 as cv
import numpy as np

categories = ['positive', 'negative', 'neutral']
DIR = os.path.join('C:', '/', 'train')

haar_cascade = cv.CascadeClassifier('haar_face.xml')

features = []
labels = []

def create_train():
    print(' ------- Training Set Initialized ------- ')
    for state in categories:
        path = os.path.join(DIR, state)
        path = path.replace("\\", '/')
        label = categories.index(state)

        for img in os.listdir(path):
            img_path = os.path.join(path, img)
            img_path = img_path.replace("\\", '/')

            img_array = cv.imread(img_path)
            gray = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)

            faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=8)
            print(f'Labeled {img_path} as {state}')
            for (x,y,w,h) in faces_rect:
                faces_roi = gray[y:y+h, x:x+w]
                features.append(faces_roi)
                labels.append(label)

create_train()

print(' ------- Training Set Created ------- ')

features = np.array(features, dtype="object")
labels = np.array(labels)

print(' ------- Training Initialized ------- ')
face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.train(features, labels)

print(' ------- Training Completed ------- ')

print(' ------- Saving... ------- ')
face_recognizer.save('readmyface_train.yml')
np.save('readmyface_features.npy', features)
np.save('readmyface_labels.npy', labels)
print(' ------- Saved! ------- ')