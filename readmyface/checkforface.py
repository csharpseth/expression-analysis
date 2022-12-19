import os
import cv2 as cv
import numpy as np

categories = ['img']#, 'neutral', 'negative']

haar_cascade = cv.CascadeClassifier('haar_face.xml')




def check_faces():
    totalChecked = 0
    totalValid = 0

    for cat in categories:
        for img in os.listdir(cat):
            img_path = cat + '/' + img

            img_array = cv.imread(img_path)
            gray = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)

            cv.imshow('checking...', gray)
            faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6)
            totalChecked+=1
            if(len(faces_rect) > 0):
                print(f'No Faces in Image: {img_path}')
                #os.remove(img_path)
            else:
                print(f'Image: {img_path} has a face')
                totalValid+=1

    print(f'Valid:{totalValid}/Total:{totalChecked}')

check_faces()