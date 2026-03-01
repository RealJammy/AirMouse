import mediapipe as mp
import numpy as np
import cv2
import time
import pyautogui
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

hand_model_path = r"tasks/hand_landmarker.task"
gesture_model_path = r"tasks/gesture_recognizer.task"
cam = cv2.VideoCapture(0)

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode



def find_avg_coords(landmarks):
    avg_x = sum([landmark.x for landmark in landmarks]) / len(landmarks)
    avg_y = sum([landmark.y for landmark in landmarks]) / len(landmarks)
    avg_z = sum([landmark.z for landmark in landmarks]) / len(landmarks)
    return avg_x, avg_y, avg_z

def avg_averages(averages):
    avg_x = sum([avg[0] for avg in averages]) / len(averages)
    avg_y = sum([avg[1] for avg in averages]) / len(averages)
    avg_z = sum([avg[2] for avg in averages]) / len(averages)
    return avg_x, avg_y, avg_z

def get_cam_coords():
    cam_width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    cam_height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
    return(cam_width, cam_height)

def calc_scalars():
    cam_coords = get_cam_coords()
    print(cam_coords)
    screen_width, screen_height = pyautogui.size()
    scalar_x = screen_width/cam_coords[0]
    scalar_y = screen_height/cam_coords[1]
    return(scalar_x, scalar_y)

def mp_to_screen_coords(mp_coords):
    scalars = calc_scalars()
    screen_width, screen_height = pyautogui.size()
    raw_x = screen_width - int(mp_coords[0] * screen_width) # Account for direction being flipped
    raw_y = int(mp_coords[1] * screen_height)
    scaled_x = raw_x*scalars[0]
    scaled_y = raw_y*scalars[1]
    print(mp_coords, scalars, (scaled_x, scaled_y))
    #print(scalars)

   # x = max(5, screen_width-5)
   # y = max(5, screen_height-5)
    #x = min(5, screen_width-5)
    #y = min(5, screen_height-5)

    x = max(5, min(screen_width, scaled_x))
    y = max(5, min(screen_height, scaled_y))
    return(x, y)


'''
def mp_to_screen_coords(mp_coords):
    # implement proper scaling lol lmao
    screen_width, screen_height = pyautogui.size()
    raw_x = screen_width - int(mp_coords[0] * screen_width) # Account for direction being flipped
    raw_y = int(mp_coords[1] * screen_height)
    
    scaled_x = int((1.28 * raw_x) - 384) # These numbers are just here to make it work for this camera. You could calibrate. We're not.
    scaled_y = int((1.28 * raw_y) - 384)
    boundary = screen_width
    # Remember to add sanity checks for the edges of the screen
    x = max(10, min(screen_width, scaled_x))
    y = max(10, min(screen_height, scaled_y))
    return (x, y)
'''

def screen_to_mp_coords(screen_coords):
    screen_width, screen_height = pyautogui.size()
    x = screen_coords[0] / screen_width
    y = screen_coords[1] / screen_height
    return (x, y)

def check_click(co_ordinates_history):
    # Simple click detection: if all coordinates are within a small range, it's a click
    x_values = sorted([coord[0] for coord in co_ordinates_history])
    y_values = sorted([coord[1] for coord in co_ordinates_history])
    if (x_values[14] - x_values[4]) < 10 and (y_values[14] - y_values[4]) < 10:
        pyautogui.click()
        return True
    return False
    

def move_mouse(x, y):
    pyautogui.moveTo(x, y)

def parse_data(result):
    #print(result.hand_landmarks[0]) # This is an array of data for the first hand detected. For each element of the array, you get x,y, and z data.
    avg_x, avg_y, avg_z = find_avg_coords(result.hand_landmarks[0])
    screen_coords = mp_to_screen_coords((avg_x, avg_y))
    co_ordinates_history.append(screen_coords)
    # Co_ordinate history is a list of 20 tuples.
    if len(co_ordinates_history) == 20:
        co_ordinates_history.pop(0)
        click_choice = check_click(co_ordinates_history)
        if click_choice:
            print("Click detected!")
            co_ordinates_history.clear() # Clear the history after a click to prevent multiple clicks from one gesture 
    move_mouse(screen_coords[0], screen_coords[1])


def print_result(result, output_image, timestamp):
    if len(result.hand_landmarks) > 0:
        parse_data(result)
    else:
        print("No hand landmarks detected.")
    #print('hand landmarker result: {}'.format(result))


options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=hand_model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

with HandLandmarker.create_from_options(options) as landmarker:
    count = 0
    co_ordinates_history = [] # This is going to be a crime against computers.
    while cam.isOpened():
        ret, frame = cam.read()
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        cv2.imshow("Camera", frame)
        landmarker.detect_async(mp_image, int(time.time() * 1000))
        cv2.waitKey(100)
        # Remove me later once we're finished testing :)
        
cv2.destroyAllWindows()