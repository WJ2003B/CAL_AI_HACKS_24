from absl import flags, app, logging
import numpy as np
import openai
import os
import io
import base64
from PIL import Image
import json
import time
import azure.cognitiveservices.speech as speechsdk
from os import path
from speech_to_text import recognize_speech, speak_text, extract_keyword


os.environ["OPENAI_API_KEY"] = "..."
client = openai.OpenAI()


def read_image(path: str):
  im = Image.open(path)
  im_np = np.array(im)
  return im_np

def encode_image(im):
  if isinstance(im, np.ndarray):
    im = Image.fromarray(im)
    buf = io.BytesIO()
    im.save(buf, format='JPEG')
    return base64.b64encode(buf.getvalue()).decode('utf-8')
  elif isinstance(im, str):
    im = Image.open(im)
    im = np.array(im)
    im = Image.fromarray(im)
    buf = io.BytesIO()
    im.save(buf, format='JPEG')
    return base64.b64encode(buf.getvalue()).decode('utf-8')
  else:
    raise NotImplementedError("You should use a np array.")
def configure_speech_recognition():
    speech_config = speechsdk.SpeechConfig(subscription="a8f58060ddcf4eeebdb3db9a07ca670f", region="eastus")
    
    speech_config.speech_recognition_language = "en-US"
    audio_in_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    audio_out_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_in_config
    )
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_out_config
    )

    return speech_recognizer, speech_synthesizer
speech_recognizer, speech_synthesizer = configure_speech_recognition()


def query(image: np.ndarray):
  with open("additional_prompt.json") as f:
    additional_prompt = json.loads(f.read())

  speech_text = recognize_speech()
  speech_text = str(speech_text)
  keyword = extract_keyword(speech_text)

  prompt_additional = additional_prompt[keyword]

  image_str = encode_image(image)
  #speech 
  messages = [{
            "role": "user",
            "content": [
              {"type": "image_url",
                 "image_url": {"url": f"data:image/jpeg:base64,{image_str}"}},
              {"type": "text",
               "text": speech_text},
                {"type": "text",
                 "text": prompt_additional}
            ],
        },]

  params = {
        "model": "gpt-4o",
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.2,
    }
  result = client.chat.completions.create(**params)
  speak =  result.choices[0].message.content 
  speak_text(speech_synthesizer, speak)
  return speak
  


   

def main(im):
  i = query(im)
  print(i)
 

if __name__=="__main__":
  while True:
    
    main("./output/captured_frame.jpg")
