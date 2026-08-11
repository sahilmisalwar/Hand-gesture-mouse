import math

class GestureController:
    """
    Takes finger states and landmarks and determines the current gesture name 
    to be acted upon.
    """
    PINCH_THRESHOLD = 40
    COOLDOWN_FRAMES = 20

    def __init__(self):
        self.cooldown_counter = 0
        self.last_gesture = "NONE"

    def get_gesture(self, finger_states, landmarks) -> str:
        """
        Determine the gesture based on finger states and landmarks.
        
        Args:
            finger_states (list[int]): [thumb, index, middle, ring, pinky]
            landmarks (list): List of 21 landmark (x, y) tuples.
            
        Returns:
            str: Gesture name ("LEFT_CLICK", "MOVE_CURSOR", "SCROLL", "RIGHT_CLICK", "NONE")
        """
        # Decrement cooldown counter if active
        if self.cooldown_counter > 0:
            self.cooldown_counter -= 1

        if not landmarks or len(landmarks) != 21:
            self.last_gesture = "NONE"
            return "NONE"

        gesture = "NONE"

        # Priority 1: Pinch detected (thumb tip close to index tip) → LEFT_CLICK
        if self._is_pinch(landmarks):
            if self.cooldown_counter == 0:
                gesture = "LEFT_CLICK"
                self.cooldown_counter = self.COOLDOWN_FRAMES
                
        # Priority 2: Only index up, rest down → MOVE_CURSOR
        elif finger_states == [0, 1, 0, 0, 0]:
            gesture = "MOVE_CURSOR"
            
        # Priority 3: Index + middle up, rest down → SCROLL
        elif finger_states == [0, 1, 1, 0, 0]:
            gesture = "SCROLL"
                
        # Priority 4: Index + middle + ring up, rest down → RIGHT_CLICK
        elif finger_states == [0, 1, 1, 1, 0]:
            if self.cooldown_counter == 0:
                gesture = "RIGHT_CLICK"
                self.cooldown_counter = self.COOLDOWN_FRAMES
                
        self.last_gesture = gesture if gesture != "NONE" else self.last_gesture
        return gesture

    def _is_pinch(self, landmarks) -> bool:
        """
        Calculates distance between thumb tip and index tip.
        """
        if len(landmarks) < 9:
            return False
            
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        
        # Euclidean distance
        distance = math.hypot(thumb_tip[0] - index_tip[0], thumb_tip[1] - index_tip[1])
        
        return distance < self.PINCH_THRESHOLD
