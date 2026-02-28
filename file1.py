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

cam = cv2.VideoCapture(0)

if cam.isOpened():
        print("Camera is ready")

cv2.waitKey()
model_path = "hand_landmarker.task"

while True:
    ret, frame = cam.read()
    if ret:
        cv2.imshow("Our image", frame)
        cv2.waitKey(1)
        

print("hi")