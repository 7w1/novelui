import requests
import os
import time
import base64
import copy
from io import BytesIO
from zipfile import ZipFile

from dotenv import load_dotenv
load_dotenv()


def annotate(model, image, low_threshold: float=None, high_threshold: float=None, distance_threshold: float=None, value_threshold: float=None):
    url = "https://api.novelai.net/ai/annotate-image"
    headers = {
        "Authorization": f"Bearer {os.environ['key']}",
        "Content-Type": "application/json"
    }

    image_b64 = base64.b64encode(image).decode('utf-8')

    data = {
        "model": model,
        "parameters": {
            "image": image_b64,
        }
    }

    if low_threshold is not None:
        data["parameters"]["low_threshold"] = low_threshold

    if high_threshold is not None:
        data["parameters"]["high_threshold"] = high_threshold

    if distance_threshold is not None:
        data["parameters"]["distance_threshold"] = distance_threshold

    if value_threshold is not None:
        data["parameters"]["value_threshold"] = value_threshold

    if 'image' in data['parameters']:
        data_copy = copy.deepcopy(data)
        data_copy['parameters']['image'] = '[image data]'
        data_str = f" and data: {data_copy}"
    else:
        data_str = f" and data: {data}"

    headers_copy = headers.copy()
    headers_copy['Authorization'] = 'Bearer [hidden]'

    print(f"Issuing request to {url} with headers: {headers_copy}{data_str}")

    start_time = time.time()
    response = requests.post(url, headers=headers, json=data)

    generation_time = time.time() - start_time
    print(f"Took {generation_time}s to annotate image.")

    try:
        image_zip = ZipFile(BytesIO(response.content))
    except:
        print(f"Error: {response} {response.content}")
        return

    return image_zip
