import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import time

detector = HandDetector(detectionCon=0.4, maxHands=1)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(3, 640)
cap.set(4, 480)

current_action = None  

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)

    hand, img = detector.findHands(img, draw=False)

    if hand and hand[0]["type"] == "Left":
        fingers = detector.fingersUp(hand[0])
        total = fingers.count(1)

        cv2.putText(img, f"Fingers: {total}", (20,40),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)

        if total == 5 and current_action != "gas":
            pyautogui.keyUp("left")
            pyautogui.keyDown("right")
            current_action = "gas"

        elif total == 0 and current_action != "brake":
            pyautogui.keyUp("right")
            pyautogui.keyDown("left")
            current_action = "brake"

        elif total not in (0, 5) and current_action is not None:
            pyautogui.keyUp("right")
            pyautogui.keyUp("left")
            current_action = None

    else:
        if current_action is not None:
            pyautogui.keyUp("right")
            pyautogui.keyUp("left")
            current_action = None

    cv2.imshow("Gesture Controller", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
