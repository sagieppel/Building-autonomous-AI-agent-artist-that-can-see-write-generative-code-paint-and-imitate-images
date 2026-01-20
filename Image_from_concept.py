# Using LLM AI agent to generate code that creates an image based on a concept

import base64, requests
from pathlib import Path
import json
API_key = "Add API Key Here: https://openrouter.ai/docs/api/reference/authentication""
output_img_path ="Dragon.png" # path to save the generated image
concept = "Monkey riding a motorcycle in the city"# concept to be generated
#"Robot turtle with mechanical legs walking on the surface of mars, in sunset"
#"complex underwater ecology with robots and animals"
prompt = "Write a generative code that generate an image of '"+concept+("'. "  
         "The code should contain a function generate(out_path) that generated image and save it into out_path."
          "Do not display the image or use any GUI functions. "
          "Your response must come as a parsable json of the following format:"
          "{'code': only code ready to execute}."
          "Return raw JSON only. Do not use Markdown, code blocks, or backticks.")
content = [{"type": "text", "text": prompt}, ]
r = requests.post(# send request to OpenRouter API
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
