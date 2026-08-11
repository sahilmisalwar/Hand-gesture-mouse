import pyautogui
import numpy as np

class MouseController:
    """
    Translates gestures and landmark positions into actual mouse actions using PyAutoGUI.
    """
    def __init__(self, frame_width=640, frame_height=480, smoothing=0.2, frame_reduction=100):
        """
        Initializes the MouseController.
        
        Args:
            frame_width (int): Webcam frame width.
            frame_height (int): Webcam frame height.
            smoothing (float): Smoothing factor (0=laggy, 1=instant).
            frame_reduction (int): Pixels to ignore on the edges for cursor mapping.
        """
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.smoothing = smoothing
        self.frame_reduction = frame_reduction
        
        self.screen_width, self.screen_height = pyautogui.size()
        self.prev_x = 0
        self.prev_y = 0
        self.scroll_prev_y = None
        
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0

    def move_cursor(self, landmark_x, landmark_y):
        """
        Moves the mouse cursor to the mapped coordinates with smoothing.
        
        Args:
            landmark_x (int): X pixel coordinate from webcam frame.
            landmark_y (int): Y pixel coordinate from webcam frame.
        """
        # Map the active frame area to screen coordinates
        screen_x = np.interp(landmark_x, (self.frame_reduction, self.frame_width - self.frame_reduction), (0, self.screen_width))
        screen_y = np.interp(landmark_y, (self.frame_reduction, self.frame_height - self.frame_reduction), (0, self.screen_height))
        
        # Apply exponential smoothing
        smooth_x = int(self.prev_x + self.smoothing * (screen_x - self.prev_x))
        smooth_y = int(self.prev_y + self.smoothing * (screen_y - self.prev_y))
        
        # Clamp to screen bounds
        smooth_x = max(0, min(smooth_x, self.screen_width - 1))
        smooth_y = max(0, min(smooth_y, self.screen_height - 1))
        
        # Move cursor
        pyautogui.moveTo(smooth_x, smooth_y)
        
        # Update previous coordinates
        self.prev_x = smooth_x
        self.prev_y = smooth_y

    def left_click(self):
        """Performs a left click."""
        pyautogui.click()

    def right_click(self):
        """Performs a right click."""
        pyautogui.rightClick()

    def double_click(self):
        """Performs a double click."""
        pyautogui.doubleClick()

    def scroll(self, current_y):
        """
        Scrolls the screen based on vertical hand movement.
        
        Args:
            current_y (int): Current Y pixel coordinate of the index finger tip.
        """
        if self.scroll_prev_y is None:
            self.scroll_prev_y = current_y
            return
        
        delta = self.scroll_prev_y - current_y
        scroll_amount = int(delta / 20)
        
        if scroll_amount != 0:
            pyautogui.scroll(scroll_amount)
        
        self.scroll_prev_y = current_y
