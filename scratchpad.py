def gesture_validation(gestures):
    return all(gesture == gestures[0] for gesture in gestures)

gestures = ["Closed_Fist", "Closed_Fist", "Closed_Fist", "Closed_Fist"]

print(gesture_validation(gestures)) 