import torch
import os
from faster_whisper import WhisperModel

class TranscriptionService:
    def __init__(self, model_size="tiny"):
        """
        Initialize Whisper model with optimized settings for Streamlit Cloud
        Use 'tiny' or 'base' model to reduce memory usage
        """
        print(f"Loading {model_size} Whisper model...")
        
        # Force CPU usage for Streamlit Cloud compatibility
        device = "cpu"
        
        # Use int8 compute type for reduced memory footprint
        compute_type = "int8"
        
        try:
            self.model = WhisperModel(
                model_size, 
                device=device,
                compute_type=compute_type,
                cpu_threads=2,  # Limit CPU threads
                num_workers=1   # Limit workers
            )
            print(f"✓ Whisper model loaded successfully on {device}")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            raise

    def transcribe(self, audio_path: str) -> str:
        """
        Transcribe audio file to text
        """
        if not os.path.exists(audio_path):
            print(f"Error: File not found - {audio_path}")
            return ""

        try:
            # Transcribe with optimized settings
            segments, info = self.model.transcribe(
                audio_path,
                beam_size=1,  # Reduce beam size for faster processing
                language="en", # Force English for faster processing
                condition_on_previous_text=False  # Disable for speed
            )
            
            print(f"Detected language: {info.language} (probability {info.language_probability:.2f})")

            full_text = ""
            for segment in segments:
                print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
                full_text += segment.text + " "
            
            return full_text.strip()
            
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""
