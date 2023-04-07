import requests
import os
import time
import base64
from io import BytesIO
from zipfile import ZipFile

from dotenv import load_dotenv
load_dotenv()


def annotate(model, image):
    url = "https://api.novelai.net/ai/annotate-image"
    headers = {
        "Authorization": f"Bearer {os.environ['key']}",
        "Content-Type": "application/json"
    }

    image_b64 = base64.b64encode(image).decode('utf-8')

    data = {"model": model, "parameters": {"image": image_b64}}

    print(f"Issuing request to {url} with headers: {headers} and data: [redacted cuz long image stuff :P]")

    start_time = time.time()
    response = requests.post(url, headers=headers, json=data)

    generation_time = time.time() - start_time
    print(f"Took {generation_time}s to generate image.")

    try:
        image_zip = ZipFile(BytesIO(response.content))
    except:
        print(f"Error: {response} {response.content}")
        return

    return image_zip
