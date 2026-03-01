import mediapipe as mp
import numpy as np
import cv2
import time
import pyautogui
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


model_path = "tasks/gesture_recognizer.task"
cam = cv2.VideoCapture(0)

BaseOptions = mp.tasks.BaseOptions
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

def mp_to_screen_coords(mp_coords):
    screen_width, screen_height = pyautogui.size()
    raw_x = screen_width - int(mp_coords[0] * screen_width) # Account for direction being flipped
    raw_y = int(mp_coords[1] * screen_height)
    scaled_x = int((1.28 * raw_x) - 384) 
    scaled_y = int((1.28 * raw_y) - 384)
    x = max(10, min(screen_width, scaled_x))
    y = max(10, min(screen_height, scaled_y))
    return (x, y)

def screen_to_mp_coords(screen_coords):
    screen_width, screen_height = pyautogui.size()
    x = screen_coords[0] / screen_width
    y = screen_coords[1] / screen_height
    return (x, y)

def check_click(co_ordinates_history):
    # Simple click detection: if all coordinates are within a small range, it's a click
    print("Checking for click...")
    x_values = sorted([coord[0] for coord in co_ordinates_history])
    y_values = sorted([coord[1] for coord in co_ordinates_history])
    if (x_values[14] - x_values[4]) < 20 and (y_values[14] - y_values[4]) < 20:
        pyautogui.click()
        return True
    return False
    
def check_line(co_ordinates_history):
    x_values = [coord[0] for coord in co_ordinates_history]
    y_values = [coord[1] for coord in co_ordinates_history]
    if abs((x_values[-1] - x_values[0])) < 50 and abs((y_values[0] - y_values[-1])) > 150:
        print("Line detected!")
        if (y_values[0] - y_values[-1]) > 0:
            # Make scroll based on change in line value
            pyautogui.scroll(1000)
        else:
            pyautogui.scroll(-1000)
        return True
    return False

def gesture_validation(gestures):
    return all(gesture == gestures[0] for gesture in gestures)


def move_mouse(x, y):
    pyautogui.moveTo(x, y)

def gesture_action(gesture):
    if gesture == "Closed_Fist":
        pyautogui.click(button="right")
        return False
    if gesture == "Pointing_Up":
        pyautogui.click()
        return False
    if gesture == "Victory":
        print("Victory detected!")
        pyautogui.click(button="middle")
        return True
    if gesture == "Thumb_Up":
        pyautogui.typewrite("Hello!")
        print("Thumbs up detected!")
        return True
    if gesture == "Thumb_Down":
        print("Thumbs down detected!")
        return True
    if gesture == "Open_Palm":
        print("Open hand detected!")
        return True  # Do not assign this action. It's our default movement state
    if gesture == "None":
        return True

def parse_data(result):
# This is an array of data for the first hand detected. For each element of the array, you get x,y, and z data.
    avg_x, avg_y, avg_z = find_avg_coords(result.hand_landmarks[0])
    screen_coords = mp_to_screen_coords((avg_x, avg_y))
    co_ordinates_history.append(screen_coords)
    shape_cache.append(screen_coords)
    # Co_ordinate history is a list of 20 tuples.
    gesture = get_gesture_result(result)
    gesture_cache.append(gesture)
    further_action = True
    click_choice = False
    if len(gesture_cache) == 10:
        if gesture != "None" and gesture_validation(gesture_cache):
            further_action = gesture_action(gesture) # We check if the user has done an implemented gesture or not.
        gesture_cache.clear()
    
    
    if len(co_ordinates_history) == 20 and further_action == True:
        print("hi!!")
        co_ordinates_history.pop(0)
        click_choice = check_click(co_ordinates_history)
        if click_choice:
            print("Click detected!")
            co_ordinates_history.clear() # Clear the history after a click to prevent multiple clicks from one gesture
            
    if len(shape_cache) == 24 and not click_choice and further_action == True: # Only check for a line if we didn't detect a click, to prevent conflicts
        shape_cache.pop(0)
        line_choice = check_line(shape_cache)
        if line_choice:
            print("Line detected!")
            shape_cache.clear()

    move_mouse(screen_coords[0], screen_coords[1])


def print_result(result, output_image, timestamp):
    if len(result.hand_landmarks) > 0:
        parse_data(result)
        gesture = get_gesture_result(result)
    else:
        print("No gesture landmarks detected.")


def get_gesture_result(category1):
    print(f"Gesture category: {category1.gestures[0][0].category_name}")
    category2 = category1.gestures[0][0].category_name
    return category2


options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    min_hand_presence_confidence=0.3,
    result_callback=print_result)

with GestureRecognizer.create_from_options(options) as recognizer:
    count = 0
    co_ordinates_history = []
    shape_cache = []
    gesture_cache = []
    while cam.isOpened():
        count += 1
        ret, frame = cam.read()
        print(count)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        cv2.imshow("Camera", frame)
        recognition_result = recognizer.recognize_async(mp_image, int(time.time() * 1000))
        if recognition_result is not None and recognition_result.gestures:
            for gesture in recognition_result.gestures:
                category = get_gesture_result(gesture[0][0])
        cv2.waitKey(100)

cv2.destroyAllWindows()

