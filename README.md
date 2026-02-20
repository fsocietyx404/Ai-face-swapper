# FaceSwap Desktop MVP – InsightFace + customtkinter

A simple desktop application with GUI that performs face swapping in videos.  
Upload your own video (mp4) and a target face image (jpg/png) → the app replaces detected faces in the video with the face from the target image.

**Current status (February 2026):** Working MVP, but requires manual model download due to insightface download issues.

## Features

- Modern dark-mode GUI using customtkinter
- Select video and target image via buttons
- GPU support (CUDA) if available, otherwise CPU fallback
- Progress bar + status messages in the GUI
- Output automatically saved as `output.mp4` in the program folder
- Threading so the GUI doesn't freeze during processing

## Important Note

This project uses **insightface** + **inswapper_128.onnx**.  
Automatic model download is unreliable / broken in many setups since 2024/2025.  
**You must manually download and place the model file** – otherwise the app will crash with "model_file ... should exist".

## Requirements

- Windows / Linux / macOS
- Python **3.10** – **3.12** (3.11 recommended)
- NVIDIA GPU + CUDA 11.8 or 12.x for much faster processing (optional but strongly recommended)

## Installation & Setup (Step-by-Step)

1. Clone the repository or download as ZIP

```bash
git clone https://github.com/YOUR_USERNAME/face_swap_app.git
cd face_swap_app

Create and activate a virtual environment (highly recommended)

Bash# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate

Install dependencies

Bashpip install -r requirements.txt

Critical: Manually download the face swap modelDownload inswapper_128.onnx (~540–555 MB) from one of these reliable sources:
https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx
https://huggingface.co/datasets/Gourieff/ReActor/resolve/main/models/inswapper_128.onnx
Place the file exactly here:textWindows:  C:\Users\YOUR_USERNAME\.insightface\models\inswapper_128.onnx
Linux:    ~/.insightface/models/inswapper_128.onnx
macOS:    ~/.insightface/models/inswapper_128.onnxCreate folders .insightface and models if they don't exist (note the leading dot!).
Start the application

Bashpython main.py
How to Use

Click "Video auswählen" / "Select Video" (MP4 file)
Click "Zielbild auswählen" / "Select Target Image" (JPG or PNG – clear face recommended)
Optional: Choose device (Auto / GPU / CPU)
Click "Start Face Swap"
Wait... (processing time depends on video length & hardware: minutes to hours)
Finished video is saved as output.mp4 in the same folder as the program

Common Issues & Fixes





























IssueSolution"model_file inswapper_128.onnx should exist"Model missing → download manually & place in ~/.insightface/modelsVery slow processingNo GPU detected? Install onnxruntime-gpu and proper CUDA toolkit"Protobuf parsing failed" / ONNX errorCorrupted download → delete file and re-downloadNo face detectedUse a target image with a very clear, frontal faceGUI freezesShouldn't happen (threading used) – check console for errors
requirements.txt
textcustomtkinter>=5.2.0
insightface>=0.7
opencv-python>=4.8
onnxruntime>=1.16          # or onnxruntime-gpu if you have CUDA
numpy>=1.24
Recommended Future Improvements

Preview of swapped first frame
Preserve original audio in output video
Option to select which face to swap if multiple detected
Batch processing for multiple videos
Adjustable quality / similarity settings

License
MIT License – feel free to use, modify, distribute (even commercially), no warranty.
Have fun swapping faces! 🚀
If you run into issues, open an issue with console output + screenshot.
