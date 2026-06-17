import cv2
import time
from services.vision_service import VisionService

def main():
    # init the Service
    service = VisionService()
    
    #Open the camera for visual inspection.
    cap = cv2.VideoCapture(0)
    print("Vision Service test has started. Press q in the video panel to exit...")
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Error: Unable to read from camera.")
            break
            
        # Running the Service's analysis on the current frame
        result = service.analyze_frame(frame)
        
        if result:
            posture = result["posture_alert"]
            mood = result["mood_alert"]
            
            # Writing statuses on the screen live so you can see what the system "thinks"
            color_posture = (0, 0, 255) if posture else (0, 255, 0)
            color_mood = (0, 0, 255) if mood else (0, 255, 0)
            
            cv2.putText(frame, f"Posture Alert (Close): {posture}", (30, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_posture, 2)
            cv2.putText(frame, f"Mood/Fatigue Alert: {mood}", (30, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_mood, 2)
        
        cv2.imshow('Testing Vision Service', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()