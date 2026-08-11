import cv2
import time
import sys
import numpy as np
from hand_tracker import HandTracker
from gesture_controller import GestureController
from mouse_controller import MouseController

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

def main():
    print("[INFO] Starting Hand Gesture Mouse... Press Q to quit.")
    
    # Try multiple camera indices
    cap = None
    for cam_index in [0, 1, 2]:
        print(f"[INFO] Trying camera index {cam_index}...")
        test_cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
        if test_cap.isOpened():
            ret, frame = test_cap.read()
            if ret and frame is not None:
                cap = test_cap
                print(f"[INFO] Camera opened successfully on index {cam_index}")
                break
            else:
                test_cap.release()
                print(f"[WARN] Camera {cam_index} opened but failed to read a frame.")
        else:
            test_cap.release()
            print(f"[WARN] Camera {cam_index} failed to open.")
    
    if cap is None:
        print("[ERROR] Could not open any camera. Please check:")
        print("  1. Your webcam is connected and not used by another app")
        print("  2. Camera drivers are installed")
        print("  3. Try closing other apps that might use the camera (Zoom, Teams, etc.)")
        input("Press Enter to exit...")
        sys.exit(1)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    
    actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"[INFO] Camera resolution: {actual_w}x{actual_h}")
    
    tracker = HandTracker(max_hands=1, detection_confidence=0.75, tracking_confidence=0.75)
    gesture_ctrl = GestureController()
    mouse_ctrl = MouseController(frame_width=FRAME_WIDTH, frame_height=FRAME_HEIGHT, smoothing=0.25)
    
    prev_time = time.time()
    
    print("[INFO] Entering main loop. Show your hand to the camera!")
    
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("[WARN] Failed to read frame, retrying...")
            time.sleep(0.1)
            continue
            
        # Flip frame horizontally (mirror effect)
        frame = cv2.flip(frame, 1)
        
        # Process frame
        frame, landmarks = tracker.detect(frame)
        
        # Calculate FPS
        curr_time = time.time()
        fps = int(1 / (curr_time - prev_time + 1e-6))
        prev_time = curr_time
        
        gesture = "NONE"
        finger_states = [0, 0, 0, 0, 0]
        
        if landmarks:
            finger_states = tracker.get_finger_states(landmarks, frame.shape)
            gesture = gesture_ctrl.get_gesture(finger_states, landmarks)
            
            if gesture == "MOVE_CURSOR":
                index_tip = tracker.get_landmark(landmarks, 8)
                mouse_ctrl.move_cursor(index_tip[0], index_tip[1])
            elif gesture == "SCROLL":
                index_tip_y = tracker.get_landmark(landmarks, 8)[1]
                mouse_ctrl.scroll(index_tip_y)
            elif gesture == "LEFT_CLICK":
                mouse_ctrl.left_click()
            elif gesture == "RIGHT_CLICK":
                mouse_ctrl.right_click()
        else:
            # Reset scroll state when no hand detected
            mouse_ctrl.scroll_prev_y = None
            
        # HUD: FPS Display
        cv2.putText(frame, f"FPS: {fps}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    
        # HUD: Gesture Label
        label = f"Gesture: {gesture}"
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)[0]
        rect_x = (FRAME_WIDTH - text_size[0]) // 2 - 10
        cv2.rectangle(frame, (rect_x, 8), (rect_x + text_size[0] + 20, 42), (0, 0, 0), -1)
        cv2.putText(frame, label, (rect_x + 10, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                    
        # HUD: Finger Indicators
        finger_names = ["T", "I", "M", "R", "P"]
        for i, (state, name) in enumerate(zip(finger_states, finger_names)):
            cx = 30 + i * 40
            cy = FRAME_HEIGHT - 30
            color = (0, 255, 100) if state else (60, 60, 60)
            cv2.circle(frame, (cx, cy), 14, color, -1)
            cv2.putText(frame, name, (cx - 6, cy + 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
                        
        # Show frame
        cv2.imshow("Hand Gesture Mouse | Press Q to quit", frame)
        
        # Break loop on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    # Cleanup
    print("[INFO] Shutting down...")
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
