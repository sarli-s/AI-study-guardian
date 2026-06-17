
import tkinter as tk
from study_facade import StudyMonitorFacade
from services.vision_service import VisionService
from services.audio_service import AudioService

live_vision = VisionService()
live_audio = AudioService(threshold=15.0)

# Create an instance of the Facade that manages everything
monitor_manager = StudyMonitorFacade(audio_service=live_audio, vision_service=live_vision)


def on_closing(root):
    """A function called when the user clicks the stop button or the X on the window"""
    monitor_manager.stop_monitoring()
    root.destroy()  

def main():    
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
    
    # 2. Running the Facade that runs all the hassles and hardware in the background in one line
    monitor_manager.start_monitoring()
    
    # 3. Activating the window loop (displays the window and leaves it open)
    root.mainloop()

if __name__ == "__main__":
    main()