import mediapipe as mp
import cv2
import time
import pyautogui
from threading import *
import tkinter as tk
from playsound3 import playsound
from screeninfo import get_monitors
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = r"hand_landmarker.task"
cam = cv2.VideoCapture(0)

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode



def find_avg_coords(landmarks):
    avg_x = sum([landmark.x for landmark in landmarks]) / len(landmarks)
    avg_y = sum([landmark.y for landmark in landmarks]) / len(landmarks)
    avg_z = sum([landmark.z for landmark in landmarks]) / len(landmarks)
    return avg_x, avg_y, avg_z

def mp_to_screen_coords(mp_coords):
    screen_width, screen_height = pyautogui.size()
    x = screen_width - int(mp_coords[0] * screen_width)
    y = int(mp_coords[1] * screen_height)
    return (x, y)

def screen_to_mp_coords(screen_coords):
    screen_width, screen_height = pyautogui.size()
    x = screen_coords[0] / screen_width
    y = screen_coords[1] / screen_height
    return (x, y)

def calibrate(result):
    print("test")
    root = tk.Tk()
    calibrate_button = tk.Button(root, text = "okay", command = calibrate())
    calibrate_button.pack()
    root.mainloop()

    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0
    avg_x, avg_y, avg_z = find_avg_coords(result.hand_landmarks[0])
    if avg_x > max_x:
        max_x = avg_x
    if avg_x < min_x:
        min_x = avg_x
    if avg_y > max_y:
        max_y = avg_y
    if avg_y < min_y:
        min_y = avg_y


def stop_if_border(x, y):
    screen_width, screen_height = pyautogui.size()
    if x > screen_width:
        print(x, screen_width)
        pyautogui.moveTo(screen_width, y)
        playsound("edge of page")
        print("success")


def move_mouse(x, y):
    stop_if_border(x, y)
    pyautogui.moveTo(x, y)

def parse_data(result):
    #print(result.hand_landmarks[0]) # This is an array of data for the first hand detected. For each element of the array, you get x,y, and z data.
    avg_x, avg_y, avg_z = find_avg_coords(result.hand_landmarks[0])
    screen_coords = mp_to_screen_coords((avg_x, avg_y))
    print(f"Average screen coordinates: x={screen_coords[0]}, y={screen_coords[1]}")
    move_mouse(screen_coords[0], screen_coords[1])


def print_result(result, output_image, timestamp, draw):
    if len(result.hand_landmarks) > 0:
        parse_data(result, draw)
    else:
        print("No hand landmarks detected.")
    #print('hand landmarker result: {}'.format(result))


def window_Tk():
    root = tk.Tk()
    calibrate_button = tk.Button(root, text = calibrate, command = calibrate())
    calibrate_button.pack()
    root.mainloop()

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

def window_CV():
    with HandLandmarker.create_from_options(options) as landmarker:
        while cam.isOpened():
            ret, frame = cam.read()
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cv2.imshow("Camera", frame)
            landmarker.detect_async(mp_image, int(time.time() * 1000))
            cv2.waitKey(125)
            # Remove me later once we're finished testing :)
        
    cv2.destroyAllWindows()

t1 = Thread(target = window_Tk)
t2 = Thread(target = window_CV)

t1.start()
t2.start()
t1.join()
t2.join()

