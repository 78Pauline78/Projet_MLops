import os
import requests
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
# Utilisation de l'URL que tu as proposée
API_URL = "https://router.huggingface.co/v1/chat/completions"

def generate_recipe(ingredients):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "messages": [
            {
                "role": "system", 
                "content": "Tu es une grand-mère française. Tu réponds uniquement en JSON valide. "
                           "N'utilise jamais de guillemets doubles (\") à l'intérieur de tes phrases, utilise des apostrophes simples ('). "
                           "L'astuce doit faire moins de 150 caractères."
            },
            {
                "role": "user", 
                "content": f"Crée une recette en JSON avec : {ingredients}. "
                           f"Structure : {{\"titre\": \"\", \"ingredients\": [], \"etapes\": [], \"astuce\": \"\"}}"
            }
        ],
        "response_format": { "type": "json_object" }, # Force le format JSON
        "max_tokens": 1000,
        "temperature": 0.1
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    return None

# print(generate_recipe("oeufs, farine, lait"))
