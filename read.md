how  to  run 

uvicorn app.main:app --reload

front  end 


C:\Users\parva\Desktop\project\faceliveness\liveness-ui
npm run dev

Below is a professional README you can directly paste.

DeepGuard-Liveness

AI-powered Face Liveness Detection Engine for preventing spoofing attacks in KYC, identity verification, and authentication systems.

This project detects whether a face presented to the camera is live or spoofed using multiple security checks such as blink detection, head movement tracking, depth validation, replay attack detection, and screen artifact detection.

🚀 Features

The engine performs multiple layers of anti-spoof detection.

1️⃣ Blink Detection

Detects natural eye blinking using Eye Aspect Ratio (EAR).

2️⃣ Head Movement Detection

Ensures the face performs slight head movements to confirm liveness.

3️⃣ Depth Validation

Analyzes facial landmark depth variance to distinguish 3D face vs flat images.

4️⃣ Micro Motion Detection

Detects subtle facial micro movements that static photos cannot reproduce.

5️⃣ Screen Artifact Detection

Detects screen moire patterns, pixel grids, and display artifacts when someone tries to show a face on another device.

6️⃣ Screen Reflection Detection

Detects reflections caused by phone or monitor displays.

7️⃣ Replay Attack Detection

Detects if the camera is viewing a video replay attack.

8️⃣ Background Validation

Checks if the environment appears natural and not synthetic.

🧠 Liveness Detection Pipeline



The engine processes each frame through a multi-layer verification system.

Camera Frame
     │
     ▼
Screen Artifact Detection
     │
     ▼
Reflection Detection
     │
     ▼
Replay Attack Detection
     │
     ▼
Micro Motion Detection
     │
     ▼
Face Detection (MediaPipe)
     │
     ▼
Blink Detection
     │
     ▼
Head Movement Detection
     │
     ▼
Depth Validation
     │
     ▼
Background Validation
     │
     ▼
Liveness Decision



🏗 Project Structure
app
 ├── core
 │    └── model_loader.py
 │
 ├── services
 │    ├── liveness_engine.py
 │    ├── depth_service.py
 │    ├── motion_service.py
 │    ├── background_service.py
 │    ├── screen_attack_detection.py
 │    ├── micro_motion_check.py
 │    ├── replay_attack_detection.py
 │    └── reflection_detection.py
 │
 └── session_manager.py



⚙️ Tech Stack
Technology	Purpose
Python	Core language
OpenCV	Video frame processing
MediaPipe FaceMesh	Facial landmark detection
NumPy	Mathematical computations
AI Vision Techniques	Anti-spoof analysis
🔍 Core Detection Methods
Eye Aspect Ratio (EAR)

Blink detection uses EAR calculated from eye landmarks.

EAR = (||p2 − p6|| + ||p3 − p5||) / (2 ||p1 − p4||)


If EAR drops below a threshold → blink detected.

Depth Variance Analysis

Facial landmarks are analyzed to measure 3D depth variation.

Flat images produce low depth variance, while real faces produce higher variance.

Micro Motion Analysis

Detects subtle facial movements across frames.

Static photos and screens do not contain these micro movements.

🛡 Attacks Prevented

This system protects against common spoofing techniques.

Attack Type	Detection Method
Photo Attack	Micro motion + Depth
Video Replay	Replay detection
Screen Attack	Screen artifact detection
Mask Attack	Depth variance
Printed Photo	Background + depth
Static Image	Blink + motion
🖥 Example Output

Example response from the engine:

{
 "status": "LIVE_VERIFIED",
 "blink_count": 3,
 "liveness": true
}


Example failure:

{
 "status": "Replay attack detected",
 "liveness": false
}

📦 Installation

Run application using :uvicorn app.main:app --reload

Note :  frontend    implimantion is  also provided
