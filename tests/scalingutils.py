import pyautogui

def mp_to_screen_coords(mp_coords):
    screen_width, screen_height = pyautogui.size()
    x = int(mp_coords[0] * screen_width)
    y = int(mp_coords[1] * screen_height)
    return (x, y)

def screen_to_mp_coords(screen_coords):
    screen_width, screen_height = pyautogui.size()
    x = screen_coords[0] / screen_width
    y = screen_coords[1] / screen_height
    return (x, y)

print(mp_to_screen_coords((0.5, 0.5)))
print(screen_to_mp_coords((1280, 720)))  