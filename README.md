# Smart Study Buddy 🧠✨

**Smart Study Buddy** is a local Python application that runs in the background, designed to improve the learning and working experience in front of the computer. The system uses artificial intelligence (AI) and computer vision to monitor the user and help maintain their health and concentration in real time — all processing runs locally on the user's computer, with no cloud services.

---

## 🚀 Main features

* **📐 Dynamic posture analysis (Posture Monitor):** Using the camera, the system detects if the user is leaning forward or sitting too close to the screen, and pops up an alert reminding them to straighten their back.
* **☕ Fatigue and drooping head detection:** A geometric algorithm detects if the user is sinking in the chair or drooping their head, and suggests taking a break or a glass of water.
* **🤖🎭 Emotion Recognition Model (Deep Learning):** A pre-trained **CNN (Convolutional Neural Network)** model in ONNX format, run locally with **ONNX Runtime**:
    * **Real-time inference:** Analyzes facial expressions directly from the webcam stream.
    * **Distress detection:** Uses the FER+ emotion model (trained on FER+, a relabeled version of the FER2013 dataset) and raises an alert when sadness or anger is detected above a confidence threshold.
    * **Network resilience:** Works in restricted environments, including filtered internet.
* **🎧 Audio Noise Control:** A continuous audio stream that measures the loudness of the background sound and detects an environment that is too noisy, recommending that the user put on headphones to stay focused.
* **💻 Independent Graphical Interface (GUI):** A small and clean window (`tkinter`) that shows the system is running and lets the user close it with a single click.
* **📦 Local & Offline AI:** The system runs entirely on the local processor, without contacting external servers or heavy cloud libraries, which ensures speed, full privacy and compatibility with strict internet filtering (an internet connection is required once, on first run, to download the emotion model).

---

## 🛠️ Project Structure

The project is built in a modular way:

* `main.py` — The main runtime file and **Composition Root** that boots up the application and sets up the GUI.
* `study_facade.py` — The system's central coordinator, implementing the **Facade Pattern**.
* `services/` — The AI services folder:
    * `IServices.py` — Abstract interfaces defining the architecture contracts (`IAudioService`, `IVisionService`).
    * `vision_service.py` — The image processing and computer vision service, implementing `IVisionService`.
    * `audio_service.py` — The audio and microphone sampling service, implementing `IAudioService`.
* `tests/` — Manual test scripts for checking each hardware component (camera, microphone) in isolation.
* `haarcascade_frontalface_default.xml` — OpenCV's face detection classifier.

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
> **Note:** On the first run, the emotion recognition model (`emotion_model.onnx`) is downloaded automatically into the current folder, so an internet connection is required once. After that, the system works fully offline.

### 3. Compiling into a standalone executable file (EXE)
To create a `main.exe` file that can be run on any Windows computer (even without Python installed):
```bash
pyinstaller --onefile --windowed main.py
```
The ready-made compiled file will be found in the `dist/` folder.

> **Note:** The application looks for `emotion_model.onnx` and `haarcascade_frontalface_default.xml` in the folder it is run from. Copy both files next to `main.exe`, or run it once with an internet connection so the model can be downloaded.

---

## 🧑‍💻 Technologies used (Tech Stack)

| Component / Domain | Technology and Implementation Path | Role in the System |
| :--- | :--- | :--- |
| **Development Language** | `Python` | The core language for managing the modular architecture of the project. |
| **Computer Vision** | `OpenCV (Haar Cascades)` | Real-time image processing, face detection, posture coordinate analysis and fatigue detection. |
| **Deep Learning Inference** | `ONNX Runtime` | Running the pre-trained CNN emotion recognition model locally on the CPU. |
| **Audio signal processing** | `Sounddevice` & `NumPy` | Continuous sampling (Audio Stream) of background noise and fast calculation of its loudness. |
| **Notifications** | `Plyer` | Displaying native desktop notifications for posture, fatigue, emotion and noise alerts. |
| **Graphical User Interface** | `Tkinter` | Python's built-in GUI library, used to display a control panel with a stop button. |
| **Parallel Task Management** | `Threading (Built-in)` | Running the microphone and camera in separate background threads so the interface stays responsive. |
| **Compiling and Distribution** | `PyInstaller` | Packaging the source code, interpreter and dependencies into a single executable file (`.exe`). |

---

## 📐 Architecture & Design Patterns

The project follows clean code principles and implements software design patterns to ensure scalability, testability, and loose coupling:

* **🔒 Singleton Pattern:** Applied to the core background services to guarantee that only a single instance of `VisionService` and `AudioService` exists during runtime. This prevents hardware resource conflicts when accessing the camera and microphone.
* **🏛️ Facade Pattern (`study_facade.py`):** Unifies the background services (Vision & Audio) and thread management under a single interface (`StudyMonitorFacade`). This decouples the presentation layer (`main.py` GUI) from the underlying hardware and AI logic (**Separation of Concerns**).
* **💉 Dependency Injection (DI):** Instead of the Facade creating its own dependencies, they are injected from the outside via the constructor (**Constructor Injection**). `main.py` acts as the **Composition Root**, creating the real hardware components and injecting them into the manager.
* **🔌 Interface-Driven Design (`IServices.py`):** Following the **D** in **SOLID** (**Dependency Inversion**), the Facade layer communicates only with abstract interfaces (`IVisionService`, `IAudioService`) rather than concrete classes. This makes it possible to replace the real services with mock implementations for isolated testing.

### ✨ Technological highlights in the architecture:
* **Local processing:** All algorithms and models run directly on the CPU of the end computer, without calls to external servers (apart from the one-time model download on first run).
* **Windowed build:** The `--windowed` option builds the application without a console window, so the user sees only the GUI and the desktop notifications.
