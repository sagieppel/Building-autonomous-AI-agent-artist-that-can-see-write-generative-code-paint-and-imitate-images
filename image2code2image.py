# This code uses OpenRouter API to generate a code that creates an image based on reference image

import base64, requests
from pathlib import Path
import json
API_key = "Add API Key Here: https://openrouter.ai/docs/api/reference/authentication"
output_img_path = "city2.png"  # path to save the generated image
input_image_path = "images/pexels-shreyas-sane-54878068-7823009.jpg" # path to the input image to be replicated
prompt = ("Look at the image and write python code that recreates the content of the image as best as possible. "
          "The code should contain a function generate(out_path) that generated image and save it into out_path."
          "Do not display the image or use any GUI functions. "
          "Your response must come as a parsable json of the following format: {'code':<only code ready to execute>,'describe':<describe what you see in the image>}.")
image_data_url = "data:image/jpeg;base64," + base64.b64encode(Path(input_image_path).read_bytes()).decode() # encode input image as data URL
content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_data_url}},
        ]
r = requests.post( # send request to OpenRouter API
    "https://openrouter.ai/api/v1/chat/completions",
    headers={"Authorization": f"Bearer {API_key}"},
    json={
        "model": "openai/gpt-5.2",
        "messages": [{
            "role": "user",
            "content": content,
        }],
    },
)
txt=r.json()['choices'][0]["message"]['content'] # get the content of the response
dic = json.loads(txt)  # parse the response as json
code = dic['code']  # get the code
namespace1 = {}
exec(code, namespace1) # execute the code
namespace1["generate"](output_img_path) # generate the image

# try: # Safer execution with error handling
#     dic = json.loads(txt)  # parse the response as json
#     code = dic['code']  # get the code
#     namespace1 = {}
#     exec(code,namespace1)
#     namespace1["generate"](output_img_path)
# except Exception as error:
#     debug_error=str(error)
#     print("Error in code execution:",debug_error)
#     print("Response was:\n",txt)
