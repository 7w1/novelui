import requests
import os
import time
import base64
import copy
from io import BytesIO
from zipfile import ZipFile

from dotenv import load_dotenv
load_dotenv()


def upscale(image, width, height, scale):
    url = "https://api.novelai.net/ai/upscale"
    headers = {
        "Authorization": f"Bearer {os.environ['key']}",
        "Content-Type": "application/json"
    }

    image_b64 = base64.b64encode(image).decode('utf-8')

    data = {
        "image": image_b64,
        "width": width,
        "height": height,
        "scale": scale
    }

    data_copy = copy.deepcopy(data)
    data_copy['image'] = '[image data]'
    data_str = f" and data: {data_copy}"

    headers_copy = headers.copy()
    headers_copy['Authorization'] = 'Bearer [hidden]'

    print(f"Issuing request to {url} with headers: {headers_copy}{data_str}")

    start_time = time.time()
    response = requests.post(url, headers=headers, json=data)

    generation_time = time.time() - start_time
    print(f"Took {generation_time}s to upscale image.")

    try:
        image_zip = ZipFile(BytesIO(response.content))
    except:
        print(f"Error: {response} {response.content}")
        return

    return image_zip