# Autonomous self improving AI Agent Artist That Can See, Write and Execute Code and improve itself
import base64, re, requests, os
import json
from pathlib import Path
from PIL import Image
import cv2
concept =  "The most amazing complex inspiring image which capture all the most beautiful patterns of nature " # concept to be generated
outdir="out_images//" # output directory
API_key = ""Add API Key Here: https://openrouter.ai/docs/api/reference/authentication"" # OpenRouter API key

if not os.path.exists(outdir): os.mkdir(outdir)
step=1
while(step<5): # limit to 5 iterations
    print("Step :",step)
    if step==1: # initial generation
        prompt = "Write a generative code that generate an image of '" + concept + ("'. "
        "The code should contain a function generate(out_path) that generated image and save it into out_path."
        "Do not display the image or use any GUI functions. "
        "Your response must come as a parsable json of the following format: {'code': only code ready to execute}.")

        content = [
            {"type": "text", "text": prompt},
        ]
    if step>1: # improve based on previous image and code
        data_url_gen_im = "data:image/jpeg;base64," + base64.b64encode(Path(gen_im_path).read_bytes()).decode()
        prompt2=(
        "You are given  generated image that tries to represent  '" + concept +
        "Followed by the code that generate this image. A"
        "analyze the  image and improve the code to better capture the concept and add details.  "
        "Do not display the image or use any GUI functions. "
        "Your response must come as a parsable json of the following format: "
        "{'code': only code ready to execute'}")#,'continue':'break'/'continue' to indicate if further improvement is needed or is the code and image are perfect'}.")
        content = [
         {"type": "text", "text": prompt2},
         {"type": "image_url", "image_url": {"url": data_url_gen_im}},
         {"type": "text", "text": code}]


    r = requests.post( # send request to OpenRouter API
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_key}"},
        json={
            #"model": "openai/gpt-5.2-mini",
            "model": "openai/gpt-5.2",
            "messages": [{
                "role": "user",
                "content": content,
            }],
        },
    )

    txt=r.json()['choices'][0]["message"]['content'] # get the content of the response
    try:
        dic = json.loads(txt)  # parse the response as json
        code = dic['code']  # get the code
        namespace1 = {}
        exec(code, namespace1) # execute the code
        gen_im_path = outdir + "//gen_text" + str(step) + ".jpg"
        namespace1["generate"](gen_im_path) # generate the image
        if not os.path.exists(gen_im_path): continue # if image not generated, retry
        step += 1
    except Exception as error: # Safer execution with error handling
        gen_im_path = outdir + "//gen_text" + str(step-1) + ".jpg" # use previous image if error
        debug_error=str(error) # get error message
        print("Error in code execution:",debug_error) # print error
        print("Response was:\n",txt) # print response
        continue

