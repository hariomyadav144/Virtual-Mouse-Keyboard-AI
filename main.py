import cv2
import mediapipe as mp
import pyautogui
import math

cap = cv2.VideoCapture(0)

screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

clicked = False
right_clicked = False
double_clicked = False

while True:
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    frame_h, frame_w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

            landmarks = hand.landmark

            index_tip = landmarks[8]
            thumb_tip = landmarks[4]
            middle_tip = landmarks[12]
            ring_tip = landmarks [16]

            x = int(index_tip.x * frame_w)
            y = int(index_tip.y * frame_h)

            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

            screen_x = screen_w / frame_w * x
            screen_y = screen_h / frame_h * y

            pyautogui.moveTo(screen_x, screen_y)

            thumb_x = int(thumb_tip.x * frame_w)
            thumb_y = int(thumb_tip.y * frame_h)

            distance = math.hypot(
                thumb_x - x,
                thumb_y - y
            )
            middle_x = int(middle_tip.x * frame_w)
            middle_y = int(middle_tip.y * frame_h)

            right_distance = math.hypot(
                thumb_x - middle_x,
                thumb_y - middle_y
            )

            cv2.line(
                frame,
                (x, y),
                (thumb_x, thumb_y),
                (255, 0, 0),
                2
            )

            if distance < 40:

                cv2.putText(
                    frame,
                    "CLICK",
                    (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

                if not clicked:
                    pyautogui.click()
                    clicked = True

            else:
                clicked = False

                if right_distance < 40:

                    cv2.putText(
                        frame,
                        "RIGHT CLICK",
                        (50,130),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 0, 0),
                        3
                    )

                    pyautogui.rightClick()

    cv2.imshow("Virtual Mouse AI", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
