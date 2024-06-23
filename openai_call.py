from absl import flags, app, logging
import numpy as np
import openai
import os
import io
import base64
from PIL import Image
import json

from os import path
from speech_to_text import recognize_speech
os.environ["OPENAI_API_KEY"] = "sk-proj-ZK8yRRgaBLaIYcTL0uPIT3BlbkFJnpWWmaBJ1IEcYAxm4dTL"
client = openai.OpenAI()

FLAGS = flags.FLAGS

# flags.DEFINE_string("prompt", None, "prompt to be fed into openai", required=True)
flags.DEFINE_string("im_dir", None, "image directory", required=True)

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

def query(image: np.ndarray):
  with open("additional_prompt.json") as f:
    additional_prompt = json.loads(f.read())

  cb_prompt_additional = str(additional_prompt["Colorblindness"])
  blindness_prompt_additional = additional_prompt["Vision_damage"]
  glaucoma_prompt_additional = additional_prompt["Glaucoma"]
  cataracts_prompt_additional = additional_prompt["Cataracts"]

  speech_text = recognize_speech
  speech_text = str(speech_text)
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
                 "text": cb_prompt_additional}
            ],
        },]

  params = {
        "model": "gpt-4o",
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.2,
    }
  result = client.chat.completions.create(**params)
  return result.choices[0].message.content 
  


   

def main(_):

  im = FLAGS.im_dir
  i = query(im)
  print(i)
 

if __name__=="__main__":
  app.run(main)
