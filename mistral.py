import os
import requests
import io
from PIL import Image

API_URL = "https://router.huggingface.co/v1/chat/completions"
headers = {
    "Authorization": "Bearer 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",
}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Exemple avec une question en français et consigne pour répondre en français
response = query({
    "messages": [
        {
            "role": "user",
            "content": "Peux-tu me donner une recette simple pour faire une omelette ?"
        }
    ],
    "model": "mistralai/Mistral-7B-Instruct-v0.2:featherless-ai"
})
print(response["choices"][0]["message"])  # Affiche la réponse

# Génération image de la recette
API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev"
headers = {
    "Authorization": "Bearer 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",
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

image_bytes = query({
    "inputs": "Une omelette dorée avec des tomates et des oignons, servie dans une assiette blanche",
})

# You can access the image with PIL.Image for example

image = Image.open(io.BytesIO(image_bytes))
image.show()  # Affiche l'image générée
image.save("omelette.png")  # Sauvegarde l'image générée
