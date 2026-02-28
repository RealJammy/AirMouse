import mediapipe as mp
import cv2
import time
import pyautogui
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = r"C:\Users\thisi\Downloads\Kek\GitHub\hack-sussex-2026\tasks\hand_landmarker.task"
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
    x = screen_width - int(mp_coords[0] * screen_width) # Account for direction being flipped
    y = int(mp_coords[1] * screen_height)
    return (x, y)

def screen_to_mp_coords(screen_coords):
    screen_width, screen_height = pyautogui.size()
    x = screen_coords[0] / screen_width
    y = screen_coords[1] / screen_height
    return (x, y)

def move_mouse(x, y):
    pyautogui.moveTo(x, y)

def parse_data(result):
    #print(result.hand_landmarks[0]) # This is an array of data for the first hand detected. For each element of the array, you get x,y, and z data.
    avg_x, avg_y, avg_z = find_avg_coords(result.hand_landmarks[0])
    screen_coords = mp_to_screen_coords((avg_x, avg_y))
    print(screen_coords)
    move_mouse(screen_coords[0], screen_coords[1])


def print_result(result, output_image, timestamp):
    if len(result.hand_landmarks) > 0:
        parse_data(result)
    else:
        print("No hand landmarks detected.")
    #print('hand landmarker result: {}'.format(result))


options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

with HandLandmarker.create_from_options(options) as landmarker:
    while cam.isOpened():
        ret, frame = cam.read()
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        cv2.imshow("Camera", frame)
        landmarker.detect_async(mp_image, int(time.time() * 1000))
        cv2.waitKey(100)
        # Remove me later once we're finished testing :)
        
cv2.destroyAllWindows()

