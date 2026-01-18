import os
import requests
import io
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"

def generate_recipe_image(recipe_title):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # Le prompt pour donner le style "Grand-mère"
    prompt = f"A rustic, professional food photography of {recipe_title}, served on a wooden table, warm lighting, grandmother's kitchen style, highly detailed."
    
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    
    if response.status_code == 200:
        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes))
        image.save("recipe_image.png")
        return "recipe_image.png"
    else:
        return f"Erreur : {response.status_code} - {response.text}"

# # Test rapide
# if __name__ == "__main__":
#     print(generate_recipe_image("Crêpes au fromage et à la fraise"))