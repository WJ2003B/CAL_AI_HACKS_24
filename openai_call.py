from absl import flags, app, logging
import numpy as np
import openai
from PIL import Image


os.environ["OPENAI_API_KEY"] = ...
client = openai.OpenAI()

FLAGS = flags.FLAGS

FLAGS.define_STRING("prompt", None, "prompt to be fed into openai", required=True)

def read_image(path: str):
  im = Image.open(path)
  im_np = np.array(im)
  return im_np

def encode_image(image: np.ndarray):
  if isinstance(im, np.ndarray):
      im = Image.fromarray(im)
      buf = io.BytesIO()
      im.save(buf, format='JPEG')
      return base64.b64encode(buf.getvalue()).decode('utf-8')
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
  im = ...
  prompt = FLAGS.prompt
  return query(prompt, im)

if __name__=="__main__":
  app.run(main)
