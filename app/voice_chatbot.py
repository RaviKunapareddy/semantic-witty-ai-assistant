import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import whisper
import pyttsx3
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wav
from sentence_transformers import SentenceTransformer
from utils.chat_core import load_vector_store, find_best_response

VECTOR_STORE_PATH = os.path.join("utils", "vector_store.pkl")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
WHISPER_MODEL = "base"  # You can change to 'small', 'medium', etc. if needed

# --- Voice Functions ---
def record_audio(duration=5, fs=16000):
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    return audio, fs

def transcribe_whisper(audio, fs, model):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav.write(f.name, fs, audio)
        result = model.transcribe(f.name)
    return result['text']

def speak_tts(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# --- Main Loop ---
import warnings
import os

def main():
    # Suppress whisper and tokenizers warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    print("\n🤖 Voice Semantic Witty Assistant is online! Say something and get sassified.")
    whisper_model = whisper.load_model(WHISPER_MODEL)
    embed_model = SentenceTransformer(EMBEDDING_MODEL)
    vector_store = load_vector_store(VECTOR_STORE_PATH)

    while True:
        audio, fs = record_audio()
        user_input = transcribe_whisper(audio, fs, whisper_model)
        if user_input:
            print(f"User: {user_input}")
        if not user_input or user_input.lower() in ["exit", "quit", "bye"]:
            print("Bot: Catch you later. I'll just be here... processing existence.")
            speak_tts("Catch you later. I'll just be here... processing existence.")
            break
        response, score = find_best_response(user_input, vector_store, embed_model)
        print(f"Bot: {response}")
        speak_tts(response)

if __name__ == "__main__":
    main()
