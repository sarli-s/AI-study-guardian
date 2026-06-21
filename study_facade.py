import cv2
import time
import threading
from plyer import notification
from services.IServices import IAudioService, IVisionService

class StudyMonitorFacade:
    def __init__(self, audio_service: IAudioService, vision_service: IVisionService): 
        # Initializing AI services behind the scenes
        #Dependency Injection
        self.running = False
        self.vision_srv = vision_service
        self.audio_srv = audio_service
        self.last_sad_alert = 0

    def start_monitoring(self):
        """Runs all monitoring systems in the background using walkers"""
        self.running = True
        
        audio_thread = threading.Thread(target=self._monitor_audio, daemon=True)
        vision_thread = threading.Thread(target=self._monitor_vision, daemon=True)
        
        audio_thread.start()
        vision_thread.start()

    def stop_monitoring(self):
        """Stops all monitoring systems"""
        self.running = False
    
    def _monitor_audio(self):
        """microphon loop in the background"""
        self.audio_srv.start_listening()
        last_audio_alert = 0
        
        try:
            while self.running:
                current_time = time.time()
                if self.audio_srv.get_status():
                    if current_time - last_audio_alert > 20:
                        notification.notify(
                            title="סביבה רועשת מדי! 🎧",
                            message="רעש הרקע חזק. אולי כדאי לשים אוזניות?",
                            app_name="SmartStudyBuddy",
                            ticker="Smart Study Buddy Alert",
                            timeout=5
                        )
                        last_audio_alert = current_time
                time.sleep(1)
        except Exception as e:
            print(f"Audio Error: {e}")
        finally:
            self.audio_srv.stop_listening()
            


    def _monitor_vision(self):
        """The camera loop in the background"""
        cap = cv2.VideoCapture(0)
        last_posture_alert = 0
        last_mood_alert = 0
        
        try:
            while cap.isOpened() and self.running:
                current_time = time.time()
                success, frame = cap.read()
                if not success:
                    time.sleep(2)
                    continue
                    
                result = self.vision_srv.analyze_frame(frame)
                if result:
                    if result["posture_alert"]:
                        if current_time - last_posture_alert > 15:
                            notification.notify(
                                title="שבי ישר! 📐",
                                message="התקרבת קצת יותר מדי למסך, כדאי ליישר את הגב.",
                                app_name="SmartStudyBuddy",
                                ticker="Smart Study Buddy Alert",
                                timeout=4
                            )
                            last_posture_alert = current_time
                    
                    if result["mood_alert"]:
                        if current_time - last_mood_alert > 30:
                            notification.notify(
                                title="צריכה הפסקה קלה? ☕",
                                message="נראה שאת קצת עייפה... מה דעתך על כוס מים?",
                                app_name="SmartStudyBuddy",
                                ticker="Smart Study Buddy Alert",
                                timeout=5
                            )
                            last_mood_alert = current_time
                            
                    # Sadness detection alert (once every 45 seconds)
                    if result.get("sad_alert") and current_time - self.last_sad_alert > 45:
                        notification.notify(
                            title="הכל טוב? נראה שקצת קשה לך... 💙",
                            message="זיהיתי ירידה באנרגיה או תסכול. מה דעתך לצאת להתאווררות קלה או להדליק מוזיקה טובה?",
                            app_name="SmartStudyBuddy",
                            timeout=7
                        )
                        self.last_sad_alert = current_time
                        
                time.sleep(1)
        except Exception as e:
            print(f"Vision Error: {e}")
        finally:
            cap.release()


