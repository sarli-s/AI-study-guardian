import cv2
import time
import threading
import tkinter as tk
from tkinter import messagebox
from plyer import notification

from services.vision_service import VisionService
from services.audio_service import AudioService

# A global variable that will tell the background loops when to stop
running = True

def monitor_audio(audio_srv):
    """The microphone is running in the background"""
    global running
    audio_srv.start_listening()
    last_audio_alert = 0
    
    try:
        while running:
            current_time = time.time()
            if audio_srv.get_status():
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
        audio_srv.stop_listening()

def monitor_vision(vision_srv):
    """The camera runs silently in the background"""
    global running
    cap = cv2.VideoCapture(0)
    last_posture_alert = 0
    last_mood_alert = 0
    
    try:
        while cap.isOpened() and running:
            current_time = time.time()
            success, frame = cap.read()
            if not success:
                time.sleep(2)
                continue
                
            result = vision_srv.analyze_frame(frame)
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
            time.sleep(1)
    except Exception as e:
        print(f"Vision Error: {e}")
    finally:
        cap.release()

def on_closing(root):
    """A function called when the user clicks the stop button or the X on the window"""
    global running
    running = False  
    root.destroy()  

def main():
    global running
    
    # 1. Creating the application's graphical window using tkinter
    root = tk.Tk()
    root.title("Smart Study Buddy")
    root.geometry("350x200")
    root.configure(bg="#f0f4f8") 
    
    title_label = tk.Label(root, text="Smart Study Buddy 🧠", font=("Arial", 16, "bold"), bg="#f0f4f8", fg="#1a365d")
    title_label.pack(pady=15)
    
    desc_label = tk.Label(root, text="המערכת פועלת כעת ברקע\nושומרת על הריכוז והיציבה שלך!", font=("Arial", 11), bg="#f0f4f8", fg="#4a5568")
    desc_label.pack(pady=5)
    
    stop_button = tk.Button(root, text="עצירת המערכת וסגירה", font=("Arial", 11, "bold"), bg="#e53e3e", fg="white", 
                            padx=10, pady=5, command=lambda: on_closing(root))
    stop_button.pack(pady=20)
    
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    
# 2. Initialize and run the AI ​​services in the background (inside processes so they don't clog the window)
    vision_srv = VisionService()
    audio_srv = AudioService(threshold=15.0)
    
    audio_thread = threading.Thread(target=monitor_audio, args=(audio_srv,), daemon=True)
    vision_thread = threading.Thread(target=monitor_vision, args=(vision_srv,), daemon=True)
    
    audio_thread.start()
    vision_thread.start()
    
    # 3. הפעלת לולאת החלון (מציג את החלון ומשאיר אותו פתוח)
    root.mainloop()

if __name__ == "__main__":
    main()