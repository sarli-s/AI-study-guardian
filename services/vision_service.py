import cv2
from services.IServices import IVisionService

class VisionService(IVisionService):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        #One-time boot
        cls._instance._initialized = False
        return cls._instance


    def __init__(self):
        if self._initialized:
            return
        # Loading the stable face classifier
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        print("[Vision Service] Local AI Service updated for high stability.")

        self._initialized = True

        
    def analyze_frame(self, frame):
        """
        Analyzes a frame stably by the location and height of the geometric face in the frame
        """
        try:
            # Get the camera dimensions (height and width of the video)
            frame_height, frame_width, _ = frame.shape
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(50, 50))
            
            posture_alert = False
            mood_alert = False
            
            if len(faces) > 0:
                (x, y, w, h) = faces[0]
                
                # 1. Posture check: If the face width is greater than 210 pixels (too close)
                if w > 210:
                    posture_alert = True
                
                # 2. Fatigue/Head Drop Test:
                # Calculate the center of the face on the Y axis
                face_center_y = y + (h / 2)
                                
                # Dynamic border: If the center of the face drops below 55% of the screen height,
                # this means the user has sunk into the chair, lowered their head, or is sprawled on the table.
                if face_center_y > (frame_height * 0.55):
                    mood_alert = True
                    
            return {
                "posture_alert": posture_alert,
                "mood_alert": mood_alert
            }
            
        except Exception as e:
            print(f"[Vision Service] Local Error: {e}")
            return None