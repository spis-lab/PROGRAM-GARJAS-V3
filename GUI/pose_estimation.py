import cv2
import mediapipe as mp
import numpy as np
from Fitur.types_of_exercise import TypeOfExercise
from Fitur.utils import *
import pandas as pd

# Fungsi untuk pra-pemrosesan gambar

class pose_estimation:
    def __init__(self):
        self.count = 0
        self.counter = 0
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.cap = cv2.VideoCapture(0)

    def detect_face_and_predict(self,olahraga,countfrom,iscount):
        self.counter = countfrom
        with self.mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:
            status = True  # state of move
            ret, frame = self.cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame.flags.writeable = False
            ## make detection
            results = pose.process(frame)
            ## recolor back to BGR
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            try:
                landmarks = results.pose_landmarks.landmark
                self.count, status = TypeOfExercise(landmarks).calculate_exercise(
                olahraga,self.count, status)
                if(self.count > 0 and status == True):
                    self.count = 0
                    self.counter = self.counter + 1

            except:
                pass
            self.mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            self.mp_drawing.DrawingSpec(color=(255, 255, 255),
                                thickness=2,
                                circle_radius=2),
            self.mp_drawing.DrawingSpec(color=(174, 139, 45),
                                thickness=2,
                                circle_radius=2),
            )
            if(iscount):
                cv2.putText(frame, "Counter : " + str(self.counter), (10, 64),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4, cv2.LINE_AA)
            return frame,self.counter

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
