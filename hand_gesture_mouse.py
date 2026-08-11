import cv2
import mediapipe as mp
import pyautogui


def run() -> None:
    pyautogui.FAILSAFE = False

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Unable to access webcam.")

    screen_w, screen_h = pyautogui.size()
    mp_hands = mp.solutions.hands

    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as hands:
        smoothed_x = None
        smoothed_y = None
        smoothing = 0.2

        while True:
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(frame_rgb)

            if result.multi_hand_landmarks:
                hand_landmarks = result.multi_hand_landmarks[0]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                target_x = int(index_tip.x * screen_w)
                target_y = int(index_tip.y * screen_h)

                if smoothed_x is None or smoothed_y is None:
                    smoothed_x, smoothed_y = target_x, target_y
                else:
                    smoothed_x = int(smoothed_x + (target_x - smoothed_x) * smoothing)
                    smoothed_y = int(smoothed_y + (target_y - smoothed_y) * smoothing)

                pyautogui.moveTo(smoothed_x, smoothed_y)

                h, w, _ = frame.shape
                cv2.circle(
                    frame,
                    (int(index_tip.x * w), int(index_tip.y * h)),
                    8,
                    (0, 255, 0),
                    -1,
                )

            cv2.imshow("Hand Gesture Mouse", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
