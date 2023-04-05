import requests
import os
import time
import textwrap
from zipfile import ZipFile
from io import BytesIO

from dotenv import load_dotenv
load_dotenv()

def generate(input: str="masterpiece", action: str="generate", model: str="nai-diffusion", width: int=512, height: int=768, scale: int=11, sampler: str="k_dpmpp_2m", steps: int=28, images: int=1, smea: bool=False, smea_dyn: bool=False, dynamic_thresholding: bool=False, controlnet_strength: int=1, legacy: bool=False, seed: int=None, negative_prompt: str="lowres"):
    url = "https://api.novelai.net/ai/generate-image"
    headers = {
        "Authorization": f"Bearer {os.environ['key']}",
        "Content-Type": "application/json"
    }

    if action == "generate":
        data = {
            "input": input,
            "model": model,
            "action": action,
            "parameters": {
                "width": width,
                "height": height,
                "scale": scale,
                "sampler": sampler,
                "steps": steps,
                "n_samples": images,
                "sm": smea,
                "sm_dyn": smea_dyn,
                "dynamic_thresholding": dynamic_thresholding,
                "controlnet_strength": controlnet_strength,
                "legacy": legacy,
                "seed": seed,
                "negative_prompt": negative_prompt
            }
        }
    else:
        return

    print(f"Issuing request to {url} with headers: {headers} and data: {data}")

    start_time = time.time()
    response = requests.post(url, headers=headers, json=data)
    try:
        image_zip = ZipFile(BytesIO(response.content))
    except:
        print(f"Error: {response} {response.content}")
        return
    generation_time = time.time() - start_time
    print(f"Took {generation_time}s to generate image.")

    return image_zip.read("image_0.png")

    dirpath = f"output/{time.strftime('%Y-%m-%d', time.localtime())}"
    filename = f"{textwrap.shorten(data['input'], width=50, placeholder='...')}-{time.strftime('%H-%M-%S', time.localtime())}.png"
    fullpath = dirpath+"/"+filename

    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    with open(fullpath, 'wb+') as f:
        f.write(image_zip.read("image_0.png"))

    image_zip.close()
    f.close()

    print(f"Image saved as {fullpath}.")

    return fullpath