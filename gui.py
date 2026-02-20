import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
from faceswap import process_video

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("FaceSwap MVP - InsightFace")
        self.geometry("700x520")
        self.resizable(False, False)
        
        self.video_path = None
        self.target_path = None
        
        # Titel
        title = ctk.CTkLabel(self, text="FaceSwap Desktop MVP", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)
        
        # Video auswählen
        self.video_btn = ctk.CTkButton(self, text="📹 Video auswählen (MP4)", width=300, height=40,
                                       command=self.select_video)
        self.video_btn.pack(pady=10)
        self.video_label = ctk.CTkLabel(self, text="Kein Video ausgewählt", text_color="gray")
        self.video_label.pack()
        
        # Zielbild auswählen
        self.target_btn = ctk.CTkButton(self, text="🖼️ Zielbild auswählen (JPG/PNG)", width=300, height=40,
                                        command=self.select_target)
        self.target_btn.pack(pady=10)
        self.target_label = ctk.CTkLabel(self, text="Kein Zielbild ausgewählt", text_color="gray")
        self.target_label.pack()
        
        # Geräteauswahl (optional)
        device_frame = ctk.CTkFrame(self)
        device_frame.pack(pady=15)
        ctk.CTkLabel(device_frame, text="Gerät:").pack(side="left", padx=10)
        self.device_var = ctk.StringVar(value="Auto")
        self.device_menu = ctk.CTkOptionMenu(device_frame, values=["Auto", "GPU", "CPU"],
                                             variable=self.device_var, width=120)
        self.device_menu.pack(side="left", padx=10)
        
        # Start Button
        self.start_btn = ctk.CTkButton(self, text="🚀 Start Face Swap", height=50, font=ctk.CTkFont(size=16, weight="bold"),
                                       fg_color="green", hover_color="darkgreen", state="disabled",
                                       command=self.start_processing)
        self.start_btn.pack(pady=20)
        
        # Progress
        self.progress = ctk.CTkProgressBar(self, width=500)
        self.progress.pack(pady=10)
        self.progress.set(0)
        
        # Status
        self.status_label = ctk.CTkLabel(self, text="Bereit – Video + Zielbild auswählen", font=ctk.CTkFont(size=14))
        self.status_label.pack(pady=10)
        
        # Output Hinweis
        hint = ctk.CTkLabel(self, text="Ausgabe: output.mp4 im Programmordner", text_color="gray")
        hint.pack(side="bottom", pady=20)
    
    def select_video(self):
        path = filedialog.askopenfilename(filetypes=[("MP4 Videos", "*.mp4")])
        if path:
            self.video_path = path
            self.video_label.configure(text=os.path.basename(path), text_color="white")
            self._check_ready()
    
    def select_target(self):
        path = filedialog.askopenfilename(filetypes=[("Bilder", "*.jpg *.jpeg *.png")])
        if path:
            self.target_path = path
            self.target_label.configure(text=os.path.basename(path), text_color="white")
            self._check_ready()
    
    def _check_ready(self):
        if self.video_path and self.target_path:
            self.start_btn.configure(state="normal")
    
    def start_processing(self):
        if not self.video_path or not self.target_path:
            return
        
        self.start_btn.configure(state="disabled")
        self.progress.set(0)
        self.status_label.configure(text="Starte Verarbeitung...")
        
        # Thread damit GUI nicht einfriert
        thread = threading.Thread(target=self._run_swap, daemon=True)
        thread.start()
    
    def _run_swap(self):
        try:
            def progress_cb(p):
                self.after(0, lambda: self.progress.set(p / 100))
            
            def status_cb(txt):
                self.after(0, lambda: self.status_label.configure(text=txt))
            
            output = process_video(
                self.video_path,
                self.target_path,
                output_path="output.mp4",
                progress_callback=progress_cb,
                status_callback=status_cb,
                device_choice=self.device_var.get()
            )
            
            self.after(0, lambda: messagebox.showinfo("Fertig!", f"Video gespeichert als:\n{os.path.abspath(output)}"))
            self.after(0, lambda: self.status_label.configure(text=f"✅ Erfolgreich! → {output}"))
            
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Fehler", str(e)))
            self.after(0, lambda: self.status_label.configure(text=f"❌ Fehler: {str(e)[:80]}..."))
        finally:
            self.after(0, lambda: self.start_btn.configure(state="normal"))
