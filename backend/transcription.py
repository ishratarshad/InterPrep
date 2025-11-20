import torch
from transformers import pipeline
import os

class TranscriptionService:
    def __init__(self, model_name="openai/whisper-small.en"):
        print(f"Loading {model_name}...")

        device = 0 if torch.cuda.is_available() else -1

        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model_name,
            device=device
        )

        print(f"✓ Ready on {'CUDA' if device == 0 else 'CPU'}")
    
    def transcribe(self, audio_path: str) -> str:
        if not os.path.exists(audio_path):
            print(f"Error: File not found - {audio_path}")
            return ""

        try:
            result = self.pipe(audio_path)
            return result["text"].strip()
        except Exception as e:
            print("Transcription error:", e)
            return ""
