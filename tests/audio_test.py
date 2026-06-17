import time
from services.audio_service import AudioService

def main():
    service = AudioService(threshold=15.0)
    
    # Enable audio streaming in the background
    service.start_listening()
    
    print("Testing has started. Make a noise to see if the status changes! Press Ctrl+C to stop.")
    
    try:
        while True:
            if service.get_status():
                print("⚠️Too noisy! Maybe you should wear headphones?")
            else:
                print("✅ quiet...")
                
            time.sleep(0.8)
    except KeyboardInterrupt:
        service.stop_listening()
        print("\The test stoped .")

if __name__ == "__main__":
    main()