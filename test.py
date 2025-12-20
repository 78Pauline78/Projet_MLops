import os
import requests

API_URL = "https://router.huggingface.co/hf-inference/models/google/vit-base-patch16-224"
headers = {
    "Authorization": "Bearer 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",
}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers={"Content-Type": "image/jpeg", **headers}, data=data)
    return response.json()

output = query("image2.jpg")


print(output)