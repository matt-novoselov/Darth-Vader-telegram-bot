from dotenv import load_dotenv
from openai import OpenAI
import os
import soundfile as sf

load_dotenv()
client = OpenAI()


async def Transcribe(file_id):
    data, samplerate = sf.read(f"Temp/{file_id}.ogg")
    sf.write(f"Temp/{file_id}.wav", data, samplerate, format='WAV', subtype='PCM_16')

    try:
        audio_file = open(f"Temp/{file_id}.wav", "rb")
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return transcript.text
    except Exception as e:
        print("[!] There was an error in transcribing voice message with Whisper: ", e)
        os.remove(f"Temp/{file_id}.ogg")
        os.remove(f"Temp/{file_id}.wav")
        return None
