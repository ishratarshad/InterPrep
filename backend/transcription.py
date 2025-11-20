import torch
from transformers import pipeline
import os
from faster_whisper import WhisperModel

class TranscriptionService:
    # def __init__(self, model_name="openai/whisper-small.en"):
    #     print(f"Loading {model_name}...")
    def __init__(self, model_size="small"):
        print(f"Loading {model_size} model...")

        # device = 0 if torch.cuda.is_available() else -1
        device = "cuda" if torch.cuda.is_available() else "cpu"

        # self.pipe = pipeline(
        #     "automatic-speech-recognition",
        #     model=model_name,
        #     device=device
        # )
        self.model = WhisperModel(model_size, device=device)

        # print(f"✓ Ready on {'CUDA' if device == 0 else 'CPU'}")
        print(f"✓ Ready on {device}")

    def transcribe(self, audio_path: str) -> str:
        if not os.path.exists(audio_path):
            print(f"Error: File not found - {audio_path}")
            return ""

        # debug/check
        segments, info = self.model.transcribe(audio_path)
        print(f"Detected language: {info.language} (probability {info.language_probability:.2f})")

        full_text = ""
        for segment in segments:
            print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
            full_text += segment.text + " "
        return full_text.strip()
