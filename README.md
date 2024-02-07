# Text-to-Math: Whisper AI, GPT-3.5

## Demo
Watch demo: https://youtu.be/inJfMOQxqEU

## Description
Some of my math classes, such as Group Theory, require me to submit homework in PDF with all equations coded in [LaTeX](https://en.wikipedia.org/wiki/LaTeX). This is not an issue when it is a small equation, but longer equations might get troublesome. That is why I decided to create this bot, that can transform my speech into Latex equation. I can then copy this equation into my editor pretty easily.

## How it works
* PyAudio records your speech, which is then saved into a WAV file.
* Whisper API gets the text from the audio file.
* GPT convert speech into LaTeX code.

## Requirements
Running this program requires that you have an OpenAI API key. You can [acquire the key](https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key) for free.

## How to Run
* Install required Python libraries:
  ```
  pip install pyaudio openai dotenv
  ```
* Create an .env file in the main directory and enter your OpenAI API key like this:
  ```
    OPENAI_API_KEY=<YOUR_KEY>
  ```
* Run the program:
  ```
    python3 main.py
  ```
* Wait for the message that the program is ready to listen:
  ```
    Listening...
  ```
* Speak your equation clearly.
* When done speaking, press Ctrl-C, and wait for the program to return the code for your equation.
  ```
    Here's the answer:

    $1 + 2 + 4 = 7 + \cos(90^\circ) = 8$           // 1 + 2 + 4 = 7 + cos(90º) = 8
  ```

## Tech Stack
* Python
* PyAudio
* Whisper AI v1
* GPT 3.5-turbo
