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
                "content": "Tu es une grand-mère française. Réponds UNIQUEMENT en JSON. Ton 'astuce' doit faire maximum 150 caractères. Structure: {'titre': '', 'ingredients': [], 'etapes': [], 'astuce': ''}"
            },
            {
                "role": "user", 
                "content": f"Fais une recette avec : {ingredients}"
            }
        ],
        "max_tokens": 1000, # On augmente la limite
        "temperature": 0.7 # Un peu de créativité pour le style 'grand-mère'
    }


    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        contenu = result['choices'][0]['message']['content']
        
        # NETTOYAGE : remplace les guillemets simples par des doubles
        contenu = contenu.replace("'", '"')
        return contenu
    return None

# print(generate_recipe("oeufs, farine, lait"))
