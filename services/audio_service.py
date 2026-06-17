import numpy as np
import sounddevice as sd

class AudioService:
    def __init__(self, threshold=15.0):
        self.threshold = threshold
        self.is_noisy = False
        self.stream = None
        print("[Audio Service] Local Stream Service Initialized.")

    def _audio_callback(self, indata, frames, time, status):
        """
        The inner loop function that calculates the noise in live
        """
        volume_norm = np.linalg.norm(indata) * 10
        
        if volume_norm > self.threshold:
            self.is_noisy = True
        else:
            self.is_noisy = False

    def start_listening(self):
        """
        Enables continuous listening in the background
        """
        try:
            self.stream = sd.InputStream(callback=self._audio_callback)
            self.stream.start()
            print("[Audio Service] Started streaming background noise...")
        except Exception as e:
            print(f"[Audio Service] Error starting stream: {e}")

    def stop_listening(self):
        """
        Close the microphone cleanly when finished.
        """
        if self.stream:
            self.stream.stop()
            self.stream.close()

    def get_status(self):
        """
        Returns whether it is currently noisy or quiet.
        """
        return self.is_noisy