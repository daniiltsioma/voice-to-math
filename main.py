# libraries
import pyaudio
from openai import OpenAI
from dotenv import load_dotenv
import os

# load environmental variables
load_dotenv()

# get OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')

# set up OpenAI client
client = OpenAI(api_key=openai_api_key)
