import cv2
import mediapipe as mp
import time

capture = cv2.VideoCapture(0)

#face detection
face_detect = mp.solutions.face_detection
structure_face = mp.solutions.drawing_utils
face_output = face_detect.FaceDetection()


pTime = 0

while True:
    success, img = capture.read()

    cv2.imshow('IMAGE',img)
    cv2.waitKey(1)

