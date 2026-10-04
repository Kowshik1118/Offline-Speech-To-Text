import json, wave
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from vosk import Model, KaldiRecognizer

MODEL_PATH = "vosk-model-small-en-us-0.15"

def browse_file():
    path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    file_entry.delete(0, tk.END); file_entry.insert(0, path)

def transcribe():
    path = file_entry.get().strip()
    if not path or not Path(path).exists():
        messagebox.showerror("Error", "Please select a valid WAV file."); return
    if not Path(MODEL_PATH).exists():
        messagebox.showerror("Error", "Vosk model not found."); return
    try:
        model = Model(MODEL_PATH); text = ""
        with wave.open(path, "rb") as audio:
            recognizer = KaldiRecognizer(model, audio.getframerate())
            while True:
                data = audio.readframes(4000)
                if len(data) == 0: break
                if recognizer.AcceptWaveform(data): text += " " + json.loads(recognizer.Result()).get("text", "")
            text += " " + json.loads(recognizer.FinalResult()).get("text", "")
        output_box.delete("1.0", tk.END); output_box.insert(tk.END, text.strip())
    except Exception as error:
        messagebox.showerror("Error", str(error))

root = tk.Tk(); root.title("Offline Speech to Text"); root.geometry("700x500")
tk.Label(root, text="Offline Speech to Text", font=("Arial", 18, "bold")).pack(pady=10)
frame = tk.Frame(root); frame.pack(fill="x", padx=15)
tk.Label(frame, text="WAV file:").pack(side="left")
file_entry = tk.Entry(frame); file_entry.pack(side="left", fill="x", expand=True, padx=8)
tk.Button(frame, text="Browse", command=browse_file).pack(side="left")
tk.Button(root, text="Convert to Text", command=transcribe, font=("Arial", 12, "bold"), bg="#2563eb", fg="white").pack(pady=10)
tk.Label(root, text="Transcript:").pack(anchor="w", padx=15)
output_box = tk.Text(root, height=12, font=("Arial", 12)); output_box.pack(fill="both", expand=True, padx=15, pady=5)
root.mainloop()
