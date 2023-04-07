import requests
import os
import time
import base64
import io

from dotenv import load_dotenv
load_dotenv()


def annotate(model, image):
    url = "https://api.novelai.net/ai/annotate-image"
    headers = {
        "Authorization": f"Bearer {os.environ['key']}",
        "Content-Type": "application/json"
    }

    bytes_io = io.BytesIO(image)

    # encode the image as a base64 string
    with open(bytes_io.read(), "rb") as f:
        image = base64.b64encode(f.read()).decode()

    data = {"model": model, "parameters": {"image": image}}

    print(f"Issuing request to {url} with headers: {headers} and data: {data}")

    start_time = time.time()
    response = requests.post(url, headers=headers, json=data)

    decoded_image = base64.b64decode(response.content)

    generation_time = time.time() - start_time
    print(f"Took {generation_time}s to generate image.")

    return decoded_image


    # Save as file
    # dirpath = f"output/{time.strftime('%Y-%m-%d', time.localtime())}"
    # filename = f"{textwrap.shorten(data['input'], width=50, placeholder='...')}-{time.strftime('%H-%M-%S', time.localtime())}.png"
    # fullpath = dirpath+"/"+filename
# 
    # if not os.path.exists(dirpath):
    #     os.makedirs(dirpath)
# 
    # with open(fullpath, 'wb+') as f:
    #     f.write(image_zip.read("image_0.png"))
# 
    # image_zip.close()
    # f.close()
# 
    # print(f"Image saved as {fullpath}.")
# 
    # return fullpath