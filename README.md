# FaceSwap Desktop MVP – InsightFace Edition

Simple desktop GUI application for face swapping in videos using InsightFace (inswapper_128).

Upload a video (mp4) + one target face image (jpg/png) → the program replaces detected faces in the video with the target face.

**Status (February 2026):** Working MVP – but **manual model download required** due to insightface download instability.

## Features

- Clean dark-mode GUI (customtkinter)
- Video & target image selection via buttons
- GPU (CUDA) support if available – huge speed difference
- Progress bar + live status messages
- Threaded processing → GUI stays responsive
- Output saved automatically as `output.mp4`

## Requirements

- Python 3.10 – 3.12 (3.11 recommended)
- Windows / Linux / macOS
- NVIDIA GPU + CUDA 11.8/12.x → **strongly recommended** for usable speed

## Installation (Step-by-Step)

1. Clone or download the repo

```bash
git clone https://github.com/YOUR_USERNAME/face_swap_app.git
cd face_swap_app

Create & activate virtual environment

Bash# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate

Install dependencies

Bashpip install -r requirements.txt

MANDATORY: Download the face swap model manuallyFile: inswapper_128.onnx (~540–555 MB)Download from (pick one – both are reliable 2026 sources):
https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx
https://huggingface.co/datasets/Gourieff/ReActor/resolve/main/models/inswapper_128.onnx
Place it exactly here:textWindows:  C:\Users\YOUR_USERNAME\.insightface\models\inswapper_128.onnx
Linux:    ~/.insightface/models/inswapper_128.onnx
macOS:    ~/.insightface/models/inswapper_128.onnx→ Create folders .insightface and models if missing
→ Leading dot is important (hidden folder)
Run the app

Bashpython main.py
How to Use

Click "Select Video" → choose .mp4 file
Click "Select Target Image" → choose .jpg or .png with clear face
Optional: choose "Auto" / "GPU" / "CPU" (GPU = much faster if you have it)
Click "Start Face Swap"
Wait (short test clip: 1–10 min, long video: 30 min – several hours on CPU)
Result: output.mp4 appears in the same folder

## Common Problems & Fixes

| Problem                                      | Fix                                                                 |
|----------------------------------------------|---------------------------------------------------------------------|
| "inswapper_128.onnx should exist"            | Model missing → download & place in `~/.insightface/models`         |
| Extremely slow / takes forever               | No GPU detected → install `onnxruntime-gpu` + CUDA toolkit          |
| "Protobuf parsing failed" or ONNX error      | Corrupted file → delete and re-download                             |
| No faces detected / bad swap quality         | Use better target image (frontal, well-lit, high-res face)          |
| App crashes without clear message            | Check console output for real error (copy & paste it into issue)    |

requirements.txt (copy-paste ready)
textcustomtkinter>=5.2.0
insightface>=0.7
opencv-python>=4.8
onnxruntime>=1.16          # ↑ install onnxruntime-gpu for NVIDIA cards
numpy>=1.24

Optional: GPU Acceleration
For 5–20× faster processing:
Bashpip uninstall onnxruntime
pip install onnxruntime-gpu

make sure you have a recent NVIDIA driver + CUDA toolkit installed.

Planned / Nice-to-have

First-frame preview
Keep original audio
Multiple faces / select which one to swap
Better error messages in GUI
Adjustable detection size / quality

MIT License – do whatever you want with it.
Note: The entire code will be translated / ported to another language/framework at some point in the future.
If it doesn't work → open an issue with:

Your OS + Python version
Console output (full traceback)
Screenshot of the error

Good luck & happy face swapping! 🚀
