from fastapi import FastAPI, Form, HTTPException, Response, UploadFile
import requests

import base64
from io import BytesIO

app = FastAPI()

def bytes_to_base64(data):
    return base64.b64encode(data).decode("utf-8")


# def img_to_base64(image_object, format="PNG"):
#     buffered = BytesIO()
#     image_object.save(buffered, format=format)
#     img_str = bytes_to_base64(buffered.getvalue())
#     return img_str

def base64_to_bytes(base64_image):
    decoded_image_data = base64.b64decode(base64_image)
    return BytesIO(decoded_image_data)

# def base64_to_img(base64_string):
#     image_stream = base64_to_bytes(base64_string)
#     img = Image.open(image_stream)
#     return img

# def open_image_to_base64(filepath):
#     img = Image.open(filepath)
#     return img_to_base64(img)
    
def generate_image_response(prompt: str, image_data: str):    

    url = 'https://travel-pose-841940665821.us-west1.run.app/api-proxy/v1beta/models/gemini-2.5-flash-image-preview:generateContent'
    payload = {
        "contents":[{"parts":[{"inlineData":{"data":image_data,"mimeType":"image/jpeg"}},{"text":prompt}]}],"generationConfig":{"responseModalities":["IMAGE","TEXT"]}
    }
    try:
        resp = requests.post(url, json=payload)
        if not resp.ok:
            status = 'Error'
            result = resp.json()
        else:
            img_list = []
            for cand in resp.json()['candidates']:
                for part in cand['content']['parts']:
                    if 'inlineData' in part:
                        img_list.append(base64_to_bytes(part['inlineData']['data']))
            print(img_list)
            if len(img_list) > 0:
                result = img_list[0]
                status = 'Success'
            else:
                result = 'image list is empty'
                status = 'Error'

    except Exception as e:
        status = 'Error'
        result = str(e)
    return {
        'status': status,
        'result': result
    }
        
    
def save_img_to_file(image, filepath):
    return image.save(filepath)
    


@app.post("/generate_image")
async def read_root(image: UploadFile, prompt: str = Form(...)):
    imges_bytes = await image.read()
    base64_image = bytes_to_base64(imges_bytes)
    response = generate_image_response(prompt,base64_image)
    print(response)
    if response['status'] == 'Success':
        return Response(response['result'].getvalue(),media_type='image/png')
    else:
        raise HTTPException(status_code=404,detail=response['result'])

