import cv2
import numpy as np
import onnxruntime as ort
from services.IServices import IVisionService
import os
import ssl
import urllib.request

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
        # 1. Stable Face Classifier Path Verification
        self.xml_path = "haarcascade_frontalface_default.xml"

        # If local XML doesn't exist, download a secure copy via unverified SSL context
        
        if not os.path.exists(self.xml_path) or os.path.getsize(self.xml_path) < 1000:
            print("[Vision Service] Creating a fresh local backup of the face XML...")
            try:
                import ssl
                import urllib.request
                context = ssl._create_unverified_context()
                backup_url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
                with urllib.request.urlopen(backup_url, context=context) as response:
                    xml_content = response.read()
                    if b"<?xml" in xml_content:
                        with open(self.xml_path, 'wb') as out_file:
                            out_file.write(xml_content)
            except Exception as e:
                print(f"[Vision Service] Network download failed: {e}")
       
        # Initialize face cascade using the verified path
        self.face_cascade = cv2.CascadeClassifier(self.xml_path)  

        # Fallback to internal OpenCV directory if local file fails to load
        if self.face_cascade.empty():
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
        # 2. Loading a deep neural network (CNN) for emotion recognition in ONNX format
        # The model is trained on the FER2013 database and recognizes: [anger, disgust, fear, joy, sadness, surprise, neutral]
        model_url = "https://github.com/onnx/models/raw/main/validated/vision/body_analysis/emotion_ferplus/model/emotion-ferplus-8.onnx"

        print("[Vision Service] Downloading/Loading Deep Learning Emotion Model (ONNX)...")
        
        self.model_path = "emotion_model.onnx"

        if not os.path.exists(self.model_path) or os.path.getsize(self.model_path) < 10000:
            print("[Vision Service] Downloading Deep Learning Emotion Model (ONNX)...")
            try:
                import ssl
                import urllib.request
                context = ssl._create_unverified_context()
                with urllib.request.urlopen(model_url, context=context) as response:
                    with open(self.model_path, 'wb') as out_file:
                        out_file.write(response.read())
            except Exception as e:
                print(f"[Vision Service] Critical Error downloading ONNX model: {e}")

        self.ort_session = ort.InferenceSession(self.model_path)
        print("[Vision Service] Deep Learning CNN Model loaded successfully!")

        self._initialized = True

        
    def analyze_frame(self, frame):
        """
        Analyzes a frame stably by the location and height of the geometric face in the frame
        AND deep-learning emotional states.
        """
        try:
            # Critical protection: prevent empty cascade from crashing the frame analysis loop
            if self.face_cascade.empty():
                return {"posture_alert": False, "mood_alert": False, "sad_alert": False}
            
            # Get the camera dimensions (height and width of the video)
            frame_height, frame_width, _ = frame.shape
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(50, 50))
            
            posture_alert = False
            mood_alert = False
            sad_alert = False
            
            # If there is at least one face in the frame   
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

                # B. Feeding the face to the neural network (Deep Learning AI)
                # Cropping the face and bringing it to the 64x64 size required by the model
                face_roi = gray[y:y+h, x:x+w]
                face_resized = cv2.resize(face_roi, (64, 64))

                # Normalize the image and adapt the structure to the grid format (Float32, Batch, Channel, H, W)
                input_data = face_resized.astype(np.float32)
                input_data = np.expand_dims(input_data, axis=0) # Add Batch
                input_data = np.expand_dims(input_data, axis=0) # Add Channel

                # Running the frame through the model layers (Forward Pass)
                input_name = self.ort_session.get_inputs()[0].name
                raw_outputs = self.ort_session.run(None, {input_name: input_data})

                # Processing the model output using the Softmax function to obtain probabilities
                scores = raw_outputs[0][0]
                exp_scores = np.exp(scores - np.max(scores))
                probabilities = exp_scores / exp_scores.sum()

                # Model indices: 0=Neutral, 1=Happiness, 2=Surprise, 3=Sadness, 4=Anger, 5=Disgust, 6=Fear, 7=Contempt
                sadness_score = probabilities[3]
                anger_score = probabilities[4]
                print(f"[AI Debug] Sadness: {sadness_score:.2f} | Anger: {anger_score:.2f} | Max Emotion Index: {np.argmax(probabilities)}")
                # If the AI ​​model detects sadness or frustration with a probability higher than 45%
                if (sadness_score > 0.45 or anger_score > 0.45): 
                    sad_alert = True

            return {
                "posture_alert": posture_alert,
                "mood_alert": mood_alert,
                "sad_alert": sad_alert
            }
        except Exception as e:
            # Silent fallback preventing thread congestion and terminal flooding
            return {"posture_alert": False, "mood_alert": False, "sad_alert": False}    
