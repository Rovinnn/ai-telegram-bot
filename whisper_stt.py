# whisper_stt.py
import whisper
from pydub import AudioSegment

# Load the model once (choose "base", "small", or "tiny" for GTX 1050)
model = whisper.load_model("base")

def transcribe_ogg(ogg_path, wav_path="voice.wav"):
    # Convert OGG to WAV
    sound = AudioSegment.from_ogg(ogg_path)
    sound.export(wav_path, format="wav")
    # Transcribe with Whisper
    result = model.transcribe(wav_path)
    return result["text"]