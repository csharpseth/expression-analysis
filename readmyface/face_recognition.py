import numpy as np
import cv2 as cv

haar_cascade = cv.CascadeClassifier('haar_face.xml')

people = ['Ben Afflek', 'Elton John', 'Jerry Seinfield', 'Madonna', 'Mindy Kaling']
features = np.load('features.npy', allow_pickle=True)
labels = np.load('labels.npy', allow_pickle=True)

Ben = 'Faces/train/Ben Afflek/3.jpg'
Jerry = 'Faces/train/Jerry Seinfield/3.jpg'
Elton = 'Faces/train/Elton John/3.jpg'

face_recognizer = cv.face.LBPHFaceRecognizer_create()

face_recognizer.read('face_train.yml')

img = cv.imread(Elton)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

for (x,y,w,h) in faces_rect:
    faces_roi = gray[y:y+h, x:x+h]

    label, confidence = face_recognizer.predict(faces_roi)
    print(f'Label: {people[label]} with Confidence: {confidence}')

    cv.putText(img, str(people[label]), (10, 10), cv.FONT_HERSHEY_TRIPLEX, 0.4, (0,0,255), 2)
    cv.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 1)

cv.imshow('Detected', img)
cv.waitKey(0)