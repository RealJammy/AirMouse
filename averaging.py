import pyautogui
import statistics
pyautogui.PAUSE = 1000000000
cursor_pos = []
#for i in range(0,2):
while True:
    prev_cursor_pos = cursor_pos
    cursor_pos.append(pyautogui.position())
    if len(cursor_pos) >= 10:
        cursor_pos.pop(0)
    #print(cursor_pos)
    recent_x = []
    for i in range(len(cursor_pos)):
        recent_x.append(cursor_pos[i].x)
    median_x = statistics.median(recent_x)
    print(median_x)