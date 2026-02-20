import os
import cv2
import urllib.request
import insightface
from insightface.app import FaceAnalysis
import onnxruntime as ort

def ensure_model():
    """Lädt das inswapper_128.onnx-Modell automatisch von Hugging Face herunter (einmalig)."""
    model_dir = os.path.expanduser("\~/.insightface/models")
    model_path = os.path.join(model_dir, "inswapper_128.onnx")
    
    if not os.path.isfile(model_path):
        os.makedirs(model_dir, exist_ok=True)
        url = "https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx"
        print("📥 Lade inswapper_128.onnx herunter (ca. 500 MB – bitte warten)...")
        urllib.request.urlretrieve(url, model_path)
        print("✅ Modell erfolgreich heruntergeladen!")
    return model_path

def get_ctx_id(device_choice: str) -> int:
    """Auto-Erkennung von GPU/CPU."""
    if device_choice == "CPU":
        return -1
    if device_choice == "GPU":
        return 0
    # Auto
    try:
        providers = ort.get_available_providers()
        return 0 if any(p.startswith("CUDA") or p.startswith("Tensorrt") for p in providers) else -1
    except:
        return -1

def init_models(ctx_id: int):
    """Initialisiert FaceAnalysis und INSwapper."""
    ensure_model()  # stellt sicher, dass Modell da ist
    
    app = FaceAnalysis(name="buffalo_l", providers=None)  # auto providers
    app.prepare(ctx_id=ctx_id, det_size=(640, 640))
    
    swapper = insightface.model_zoo.get_model("inswapper_128.onnx", download=False)
    return app, swapper

def swap_faces_in_frame(frame, app, swapper, source_face):
    """Ersetzt alle erkannten Gesichter im Frame mit dem Zielgesicht."""
    faces = app.get(frame)
    if not faces:
        return frame  # kein Gesicht → Originalframe zurück
    
    for face in faces:
        frame = swapper.get(frame, face, source_face, paste_back=True)
    return frame

def process_video(
    video_path: str,
    target_image_path: str,
    output_path: str = "output.mp4",
    progress_callback=None,
    status_callback=None,
    device_choice: str = "Auto"
):
    """
    Hauptfunktion: Video Face-Swap.
    - progress_callback: float 0-100
    - status_callback: str
    """
    ctx_id = get_ctx_id(device_choice)
    
    if status_callback:
        status_callback("🔄 Initialisiere Modelle...")
    
    app, swapper = init_models(ctx_id)
    
    # Zielgesicht laden (Zielbild)
    target_img = cv2.imread(target_image_path)
    if target_img is None:
        raise ValueError("❌ Zielbild konnte nicht geladen werden!")
    
    target_faces = app.get(target_img)
    if not target_faces:
        raise ValueError("❌ Kein Gesicht im Zielbild erkannt!")
    
    # Größtes Gesicht als Quelle nehmen (beste Qualität)
    source_face = max(target_faces, key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]))
    
    # Video öffnen
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("❌ Video konnte nicht geöffnet werden!")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        swapped = swap_faces_in_frame(frame, app, swapper, source_face)
        writer.write(swapped)
        
        frame_count += 1
        if progress_callback and frame_count % 10 == 0:  # nicht bei jedem Frame updaten
            progress = (frame_count / total_frames) * 100
            progress_callback(progress)
        
        if status_callback and frame_count % 30 == 0:
            status_callback(f"Verarbeite Frame {frame_count}/{total_frames} ({progress:.1f}%)")
    
    cap.release()
    writer.release()
    
    if progress_callback:
        progress_callback(100)
    if status_callback:
        status_callback(f"✅ Fertig! Video gespeichert als {output_path}")
    
    return output_path
