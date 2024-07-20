import pyaudio
import wave
import speech_recognition as sr
from gtts import gTTS
import pygame
import google.generativeai as genai
genai.configure(api_key="")
model = genai.GenerativeModel('gemini-1.0-pro-latest')

# print("Recording...")
while True:
    # Set parameters for audio stream
    CHUNK = 1024          # Number of audio samples per buffer
    FORMAT = pyaudio.paInt16  # Audio format (16-bit integer)
    CHANNELS = 1          # Number of audio channels (1 for mono)
    RATE = 44100          # Sampling rate (samples per second)
    RECORD_SECONDS = 4   # Duration to record
    WAVE_OUTPUT_FILENAME = 'output.wav'
    WAVE_OUTPUT_FILENAME = 'output.wav'
    TEXT_OUTPUT_FILENAME = 'output.mp3'
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open audio stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Recording...")
    frames = []

    try:
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
    except KeyboardInterrupt:
        print("Stopped Recording")

    print("Finished recording")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data to a WAV file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Saved recording to {WAVE_OUTPUT_FILENAME}")

    # Convert audio to text
    recognizer = sr.Recognizer()

    with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        print("Converted audio to text:")
        print(text)
        if "ok google" in text.lower():
            print("The phrase 'OK Google' was detected in the audio.")
            break
        else:
            print("The phrase 'OK Google' was not detected in the audio.")
        text1=model.generate_content(text).text
        print(text1)
        tts = gTTS(text=text1, lang='en')
        tts.save(TEXT_OUTPUT_FILENAME)
        print(f"Converted text to audio and saved to {TEXT_OUTPUT_FILENAME}")

        # Play the converted audio file
        pygame.mixer.init()
        pygame.mixer.music.load(TEXT_OUTPUT_FILENAME)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            continue
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        
        
print("Welcome to the Server")
