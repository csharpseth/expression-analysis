import numpy as np
import cv2 as cv
import requests

""" haar_cascade = cv.CascadeClassifier('haar_face.xml')

categories = ['positive', 'negative']
features = np.load('features.npy', allow_pickle=True)
labels = np.load('labels.npy', allow_pickle=True)



for (x,y,w,h) in faces_rect:
    faces_roi = gray[y:y+h, x:x+h]

    label, confidence = face_recognizer.predict(faces_roi)
    print(f'Label: {people[label]} with Confidence: {confidence}')

    cv.putText(img, str(people[label]), (10, 10), cv.FONT_HERSHEY_TRIPLEX, 0.4, (0,0,255), 2)
    cv.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 1)
 """

#Live Feed
capture = cv.VideoCapture(0)

def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width,height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

def changeRes(width, height):
    capture.set(3, width)
    capture.set(4, height)

changeRes(640, 640)

haar_cascade = cv.CascadeClassifier('haar_face.xml')
categories = ['positive', 'negative', 'neutral']
features = np.load('readmyface_features.npy', allow_pickle=True)
labels = np.load('readmyface_labels.npy', allow_pickle=True)

#Face Recognition
face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read('readmyface_train.yml')

isFace = False

numFrames = 1
numFramesTo = 3

numPositive = 1
numNegative = 1
numNeutral = 1

currentSentiment = 2

def analyzeSentiment(sentiment):
    global numFrames, numPositive, numNegative, numNeutral, currentSentiment, numFramesTo

    numFrames+=1

    if (sentiment == 0):
        numPositive+=1
    if(sentiment == 1):
        numNegative+=1
    if(label == 2):
        numNeutral+=1

    if(numFrames >= numFramesTo):
        if(numPositive > numNegative & numPositive >= numNeutral):
            currentSentiment = 0
            resetSentimentNormalizer()
        else:
            if(numNegative > numPositive & numNegative >= numNeutral):
                currentSentiment = 1
                resetSentimentNormalizer()
            else:
                currentSentiment = 2
                resetSentimentNormalizer()

def resetSentimentNormalizer():
    global numFrames, numPositive, numNegative, numNeutral
    numPositive = 0
    numNegative = 0
    numNeutral = 0
    numFrames = 0

while True:
    isTrue, frame = capture.read()

    #convert to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #find all faces in the given frame
    faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8)

    #these are use to narrow down the face detection to one face
    start_x = 0
    start_y = 0
    width = 0
    height = 0

    #check if there is even a face present in the frame
    if (len(faces_rect) > 0):
        isFace = True
    else:
        isFace = False

    #initialize the label and default it to neutral(at index of 2)
    label = 2
    confidence = 0.0

    if (isFace == True):
        #iterates through all of the detected faces and picks the closest one based on the size of the rectangle
        for (x,y,w,h) in faces_rect:
            if (w>=width):
                width = w
                height = h
                start_x = x
                start_y = y
        #draw a rectangle around every detected face
        cv.rectangle(frame, (start_x,start_y), (start_x+width,start_y+height), (0, 255, 0), thickness=1)
        
        faces_roi = gray[start_y:start_y+height, start_x:start_x+width]
        label, confidence = face_recognizer.predict(faces_roi)
        analyzeSentiment(label)

    req = requests.post("http://localhost/sentiment?s=%s&f=%s" % (categories[currentSentiment], isFace))

    #Background
    cv.rectangle(frame, (0,0), (180,40), (0,0,0), -1)
    #Is a face detected label
    cv.putText(frame, f'Face Detected: {isFace}', (6, 12), cv.FONT_HERSHEY_TRIPLEX, 0.4, (255, 255, 255), thickness=1)
    #The current sentiment of a detected face
    cv.putText(frame, f'Face Sentiment: {categories[currentSentiment]}', (6, 24), cv.FONT_HERSHEY_TRIPLEX, 0.4, (255, 255, 255), thickness=1)
    #The confidence of that sentiment
    cv.putText(frame, f'Confidence: {int(confidence)}', (6, 36), cv.FONT_HERSHEY_TRIPLEX, 0.4, (255, 255, 255), thickness=1)

    cv.imshow('face detect', frame)

    if(cv.waitKey(20) & 0xFF==ord('d')):
        break

capture.release()
cv.destroyAllWindows()