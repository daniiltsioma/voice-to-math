# libraries
import pyaudio
from openai import OpenAI
from dotenv import load_dotenv
import wave
import os
import io

# load environmental variables
load_dotenv()

# get OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')

# set up OpenAI client
client = OpenAI(api_key=openai_api_key)

# recording limit (30 seconds)
RECORD_SECONDS = 30

# pyaudio params
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000                    # required for Whisper AI
CHUNK = 1024

# initializae pyaudio
p = pyaudio.PyAudio()

# create a recording stream
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=CHUNK)

print("Hello! This is your friendly voice-to-math bot. I will convert your spoken text into LaTeX code.")

print("\nYou can start speaking now! Press Ctrl-C when you're done.")
print("Listening...")

frames = []

# record audio in WAV file
try:
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

# ctrl-c pressed - stop recording
except KeyboardInterrupt:
    print("Recording done.")

finally:
    print("Analyzing recording...")

    # stop and close the stream
    stream.stop_stream()
    stream.close()
    # terminate pyaudio instance
    p.terminate()

    # store audio bytes in memory
    audio_buffer = io.BytesIO()

    # save audio data into WAV object
    wf = wave.open(audio_buffer, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # for now, I did not find a way to send audio data to
    # Whisper API before writing it into a file beforehand.
    # When I do, I will edit this code in the repository.

    # remove previous recording file in the folder if it exists
    if os.path.exists('rec.wav'):
        os.system('rm rec.wav')

    # write audio into a WAV file
    with open('rec.wav', 'bx') as f:
        f.write(audio_buffer.getvalue())

    # open newly-written file, 'read binary' mode
    wav = open('rec.wav', 'rb')

    # get transcript from Whisper
    transcript = client.audio.transcriptions.create(
        model='whisper-1',
        file=wav
    )

    # close the file
    wav.close()

    # get the text from the file to use as a GPT prompt
    prompt = transcript.text

    print("GPT is converting your request...")

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                # we are sending a question as a user
                'role': 'user',
                # request GPT to convert prompt
                'content':  f'send this text back, with math terms converted into Latex: {prompt}.'
            }
        ]
    )

    # GPT might send multiple options for answers,
    # we are going to use the best one
    print("Here's the answer:\n")

    print(response.choices[0].message.content)
