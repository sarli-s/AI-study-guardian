from abc import ABC, abstractmethod

class IAudioService(ABC):
    @abstractmethod
    def start_listening(self):
        pass

    @abstractmethod
    def stop_listening(self):
        pass

    @abstractmethod
    def get_status(self) -> bool:
        pass


class IVisionService(ABC):
    @abstractmethod
    def analyze_frame(self, frame) -> dict:
        pass