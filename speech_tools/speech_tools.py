import io
import os

import pydub
import speech_recognition
from gtts import gTTS

from setup.setup import DATA_PATH


def speech2text_me(file_path):
    f = pydub.AudioSegment.from_file(io.BytesIO(file_path)).export(format="wav")
    recognator = speech_recognition.Recognizer()
    with speech_recognition.AudioFile(f) as source:
        audio_data = recognator.record(source)
    out = recognator.recognize_google(audio_data, language="ru")
    return out


def text2speech_me(chat_id, input):
    # todo https://www.codingem.com/best-ai-voice-generators/
    voice = gTTS(text=input, lang="en", slow=False)
    voice_file = os.path.join(DATA_PATH, str(chat_id) + ".ogg")
    voice.save(voice_file)
    voice = open(voice_file, "rb")
    return voice
