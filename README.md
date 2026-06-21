# Smart Study Buddy 🧠✨

**Smart Study Buddy** is a local and smart Python application that runs in the background, designed to improve the learning and working experience in front of the computer. The system uses artificial intelligence (AI) and computer vision technologies to monitor the user and maintain their health and concentration in real time, regardless of the Internet connection (bypasses NetFri blocks by 100%).

---

## 🚀 Main features

* **📐 Dynamic posture analysis (Posture Monitor):** Using the camera, the system detects if the user is leaning forward or dangerously close to the screen, and pops up an alert essential for straightening the back.
* **☕ Fatigue and drooping head detection:** A geometric algorithm detects if the user is sinking in the chair or drooping their head due to lack of strength, and suggests taking a break or a glass of water.
* ** 🤖🎭 Advanced Emotion Recognition Model (Deep Learning)
The system now includes an offline-capable, high-performance **Deep Learning CNN (Convolutional Neural Network) Model** using **ONNX Runtime**:
    * Real-time Inference:** Analyzes facial expressions directly through the webcam stream with sub-millisecond processing times.
    * Smart Distress Detection:** Trained on the FER2013 dataset, specifically calibrated to identify frustration, anger, and sadness with a confidence score threshold.
    * Network & SSL Resilience:** Features automatic SSL bypass and dynamic fallback handlers, allowing stable downloads and fully offline operation in strictly restricted environments (e.g., filtered internet).
* **🎧 Audio Noise Control:** A continuous audio service (Audio Stream) that analyzes the signal strength (RMS) and identifies an environment that is too noisy, to recommend that the user put on headphones to maintain concentration.
* **💻 Independent Graphical Interface (GUI):** A small and clean window (`tkinter`) that allows the user to see that the system is running, and to easily close it with a single click.
* **📦 Completely independent (Local & Offline AI):** The system runs entirely on the local processor, without contacting external servers or heavy cloud libraries, which ensures peak speed, full privacy and compatibility with strict internet filtering.

---

## 🛠️ Project Structure

The project is built in a modular and professional way:

* `main.py` — The main runtime file and **Composition Root** that boots up the application and sets up the GUI.
* `study_facade.py` — The system's central coordinator executing the **Facade Pattern**.
* `services/` — The AI services folder:
    * `IServices.py` — Abstract interfaces establishing the architecture contracts (`IAudioService`, `IVisionService`).
    * `vision_service.py` — The image processing and computer vision service implementing `IVisionService`.
    * `audio_service.py` — The audio and microphone sampling service implementing `IAudioService`.
* `tests/` — Independent test and runtime files for each hardware component in isolation.
---


## ⚙️ Instructions for operation and running

### 1. Installing prerequisites
Make sure you have Python installed, and run the following command in the terminal to install all the necessary libraries:
```bash
pip install -r requirements.txt
```
### 2. Running the application
To run the system from the source code:
```bash
python main.py
```

### 3. Compiling into a standalone executable file (EXE)
To create a main.exe file that can be run on any Windows computer (even without Python installed):
```bash
pyinstaller --onefile --windowed main.py
```
The ready-made compiled file will be found in the dist/ folder.

## 🧑‍💻 Technologies used (Tech Stack)

| Component / Domain | Technology and Implementation Path | Role in the System |
| :--- | :--- | :--- |
| **Development Language** | `Python` | The core language for managing the modular architecture of the project. |
| **Artificial Intelligence and Computer Vision** | `OpenCV (Haar Cascades)` | Real-time silent image processing, face recognition, posture coordinate analysis and fatigue index detection. |
| **Audio signal processing** | `Sounddevice` & `NumPy` | Continuous sampling (Audio Stream) of background noise and fast mathematical calculation of signal strength (RMS). |
| **Graphical User Interface** | `Tkinter` | Python's built-in GUI library used to display a designed control panel and a built-in stop button. |
| **Parallel Task Management** | `Threading (Built-in)` | Running the microphone and camera in separate background processes (Multitasking) to prevent the main interface from crashing. |
| **Compiling and Distribution** | `PyInstaller` | Packaging all source code, interpreter and dependencies into a single, independent binary executable file (`.exe`). |

---

---

## 📐 Architecture & Design Patterns

The project follows clean code principles and strictly implements advanced software design patterns to ensure scalability, testability, and loose coupling:

* **🔒 Singleton Pattern:** Applied to the core background services to guarantee that only a single instance of `VisionService` and `AudioService` exists during runtime. This prevents critical hardware resource conflicts when accessing the camera and microphone.
* **🏛️ Facade Pattern (`study_facade.py`):** Unified the background services (Vision & Audio) and thread management under a single interface (`StudyMonitorFacade`). This decouples the presentation layer (`main.py` GUI) entirely from the complex underlying hardware and AI execution logic (**Separation of Concerns**).
* **💉 Dependency Injection (DI):** Instead of the Facade creating its own dependencies, they are injected from the outside via the constructor (**Constructor Injection**). `main.py` acts as the **Composition Root**, instantiating the real hardware components and injecting them into the manager.
* **🔌 Interface-Driven Design (`IServiced.py`):** Embracing the **D** in **SOLID** principles (**Dependency Inversion**), the Facade layer communicates exclusively with abstract interfaces (`IVisionService`, `IAudioService`) rather than concrete classes. This allows seamless mocking for isolated automated testing in the `tests/` folder.


### ✨ Technological highlights in the architecture:
* **Local processing (100% Offline):** All libraries and algorithms run directly on the CPU of the end computer, without the need for the Internet or calls to external servers (fully bypasses filtering blocks).
* **Improved stability in compilation:** The application supports the `--windowed` mechanism that allows smooth activation of internal notifications from the UI directly on top of all other system windows of the user.