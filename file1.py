import mediapipe as mp
import cv2
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

model_path = r"c:\Users\emily\AppData\Local\python\pythoncore-3.14-64\hand_landmarker.task"

cam = cv2.VideoCapture(1)

while cam.isOpened():
    ret, frame = cam.read()
    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cv2.imshow("Camera", frame)


print("hi")