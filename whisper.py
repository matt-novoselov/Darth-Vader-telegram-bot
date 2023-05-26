from dotenv import load_dotenv
import openai
import os
import subprocess

load_dotenv()
openai.api_key = os.getenv('OPENAI_TOKEN')


async def Transcribe(file_id):
    subprocess.call(['ffmpeg', '-i', f"Temp/{file_id}.ogg", f"Temp/{file_id}.wav"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,)

    try:
        audio_file = open(f"Temp/{file_id}.wav", "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript["text"]
    except Exception as e:
        print("[!] There was an error in transcribing voice message with Whisper: ", e)
        os.remove(f"Temp/{file_id}.ogg")
        os.remove(f"Temp/{file_id}.wav")
        return None
