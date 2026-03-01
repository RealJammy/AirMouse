import pyautogui
import time


def move_mouse(x, y):
    pyautogui.moveTo(x, y)

def move_and_click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    
def move_top_right():
    width, height = pyautogui.size()
    pyautogui.moveTo(width - 10, 0) # To deal with the failsafe

def drag_mouse(start_coords, end_coords):
    pyautogui.moveTo(start_coords[0], start_coords[1])
    pyautogui.dragTo(end_coords[0], end_coords[1], duration=1)

def move_and_scroll_mouse(start_coords, amount):
    pyautogui.moveTo(start_coords[0], start_coords[1])
    pyautogui.scroll(amount)

time.sleep(5) 
move_and_scroll_mouse((200, 400), -100)