import cv2
import mediapipe as mp

class HandTracker:
    """
    Wraps MediaPipe Hands detection logic. Detects hand landmarks from a webcam frame 
    and exposes them cleanly to other modules.
    """
    def __init__(self, max_hands=1, detection_confidence=0.75, tracking_confidence=0.75):
        """
        Initializes the HandTracker.
        
        Args:
            max_hands (int): Max number of hands to detect.
            detection_confidence (float): Min detection confidence.
            tracking_confidence (float): Min tracking confidence.
        """
        self.mp_hands = mp.solutions.hands
        self.drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

    def detect(self, frame):
        """
        Detects hands in the given frame.
        
        Args:
            frame: BGR frame from OpenCV.
            
        Returns:
            tuple: (annotated_frame, list_of_landmarks)
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        landmarks_list = []
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                h, w, c = frame.shape
                for lm in hand_landmarks.landmark:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmarks_list.append((cx, cy))
                
                # Only process the first hand detected
                break
                
        return frame, landmarks_list

    def get_finger_states(self, landmarks, frame_shape):
        """
        Determines which fingers are raised.
        
        Args:
            landmarks (list): List of 21 landmark (x, y) tuples.
            frame_shape (tuple): Frame dimensions.
            
        Returns:
            list[int]: [thumb_up, index_up, middle_up, ring_up, pinky_up]
        """
        if not landmarks or len(landmarks) != 21:
            return [0, 0, 0, 0, 0]
            
        fingers = []
        
        # Thumb
        # Determine hand orientation using wrist (0) and pinky mcp (17) or index mcp (5)
        # Using the prompt's suggestion: "compare x coordinates (handle both left and right hand using wrist x)"
        wrist_x = landmarks[0][0]
        index_mcp_x = landmarks[5][0]
        
        # If index_mcp_x > wrist_x, hand is pointing right-ish (right hand back, or left hand palm)
        # We can just check the distance of tip(4) and ip(3) from wrist(0) or just compare 4 and 3 based on hand side
        is_right_side = index_mcp_x > wrist_x
        if is_right_side:
            thumb_up = 1 if landmarks[4][0] > landmarks[3][0] else 0
        else:
            thumb_up = 1 if landmarks[4][0] < landmarks[3][0] else 0
            
        fingers.append(thumb_up)
        
        # Other fingers: tip (8, 12, 16, 20) vs pip/mcp (6, 10, 14, 18)
        # For fingers, if tip y < pip y -> finger is up
        tip_ids = [8, 12, 16, 20]
        pip_ids = [6, 10, 14, 18]
        
        for tip, pip in zip(tip_ids, pip_ids):
            if landmarks[tip][1] < landmarks[pip][1]:
                fingers.append(1)
            else:
                fingers.append(0)
                
        return fingers

    def get_landmark(self, landmarks, index):
        """
        Gets the (x, y) coordinates of a specific landmark.
        
        Args:
            landmarks (list): List of landmarks.
            index (int): Landmark index.
            
        Returns:
            tuple: (x, y) pixel coordinates.
        """
        if landmarks and 0 <= index < len(landmarks):
            return landmarks[index]
        return (0, 0)
