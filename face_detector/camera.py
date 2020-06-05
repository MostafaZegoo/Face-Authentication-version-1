#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 01:28:21 2020

@author: mostafa
"""

import cv2,os
from django.conf import settings
import face_recognition

face_detection_videocam = cv2.CascadeClassifier(os.path.join(
            settings.BASE_DIR,'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        process_this_frame = True
        
        if process_this_frame:
            success, image = self.video.read()
            # We are using Motion JPEG, but OpenCV defaults to capture raw images,
            # so we must encode it into JPEG in order to correctly display the
            # video stream.
            
            face_1_image = face_recognition.load_image_file("face_detector/mostafa.jpg")
            face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor = 1.3, minNeighbors = 5)
            
            for (x, y, w, h) in faces_detected:
                small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]
                
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                    
                check = face_recognition.compare_faces(face_1_face_encoding, face_encodings)
    
                if check[0]:
                    result = "Mostafa"
                else:
                    result = "Unknown"
                
                image = cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color = (255, 0, 0), thickness = 2)
                image = cv2.flip(image, 1)
                image = cv2.putText(image, result, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.9, color = (3,255,12), thickness = 2)
    
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()
        
        process_this_frame = not process_this_frame