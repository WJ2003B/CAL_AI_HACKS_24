from absl import flags, app, logging
import numpy as np
import openai
import os
import io
import base64
from PIL import Image


os.environ["OPENAI_API_KEY"] = "sk-proj-ZK8yRRgaBLaIYcTL0uPIT3BlbkFJnpWWmaBJ1IEcYAxm4dTL"
client = openai.OpenAI()

FLAGS = flags.FLAGS

FLAGS.define_STRING("prompt", None, "prompt to be fed into openai", required=True)
FLAGS.define_STRING("im_dir", None, "image directory", required=True)

def read_image(path: str):
  im = Image.open(path)
  im_np = np.array(im)
  return im_np

def encode_image(im: np.ndarray):
  if isinstance(im, np.ndarray):
      im = Image.fromarray(im)
      buf = io.BytesIO()
      im.save(buf, format='JPEG')
      return base64.b64encode(buf.getvalue()).decode('utf-8')
  else:
    raise NotImplementedError("You should use a np array.")

def query(prompt: str, image: np.ndarray):
  image_str = encode_image(image)
  
  messages = [{
            "role": "user",
            "content": [
              {"type": "image_url",
                 "image_url": {"url": f"data:image/jpeg:base64,{image_str}"}},
                {"type": "text",
                 "text": prompt}
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
  prompt = FLAGS.prompt
  return query(prompt, im)

if __name__=="__main__":
  app.run(main)
