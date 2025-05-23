import os
from dotenv import load_dotenv
import imageio_ffmpeg as ffmpeg
import openai

# Set FFmpeg binary to the one from imageio_ffmpeg
os.environ["FFMPEG_BINARY"] = ffmpeg.get_ffmpeg_exe()

# 모델 설정
model_name = 'gpt-3.5-turbo'

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from .env
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
  raise ValueError("OPENAI_API_KEY not found in .env file")

openai.api_key = openai_api_key
