from openai import OpenAI




def transcribe_audio(file_path):
    client = OpenAI()
    audio_file= open(file_path, "rb")

    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file)
    

    return transcription.text


if __name__ == "__main__":
 #test
    text = transcribe_audio("audio.wav")
    print("\n--- TRANSCRIPT ---")
    print(text)