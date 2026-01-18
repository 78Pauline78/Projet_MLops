import json
import re
from app.llm.recette_gen import generate_recipe
from app.image.image_gen import generate_recipe_image
from app.pdf.pdf_builder import generer_pdf_recette

def nettoyer_json(raw_text):
    # Enlève les balises Markdown si présentes
    clean = re.sub(r'```json|```', '', raw_text).strip()
    # Remplace les apostrophes simples par des courbes pour ne pas casser le JSON
    # mais seulement si elles sont entourées de texte (ex: l'huile -> l’huile)
    clean = clean.replace("'", "’")
    # Tente de restaurer les guillemets doubles nécessaires au JSON (approche simple)
    clean = clean.replace("’titre’", '"titre"').replace("’ingredients’", '"ingredients"')
    clean = clean.replace("’etapes’", '"etapes"').replace("’astuce’", '"astuce"')
    return clean

def fabriquer_ma_recette(liste_ingredients):
    print("1. Génération de la recette texte...")
    recette_json_raw = generate_recipe(liste_ingredients)

    try:
        # Nettoyage et conversion
        clean_json = nettoyer_json(recette_json_raw)
        recette = json.loads(clean_json)

        print(f"2. Génération de l'image pour : {recette['titre']}...")
        image_path = generate_recipe_image(recette['titre'])

        print("3. Création du PDF...")
        generer_pdf_recette(recette, image_path)

        print("Terminé ! Ton PDF est prêt.")

    except json.JSONDecodeError as e:
        print(f"Erreur de formatage auto-corrigée : {e}")
        print("Réessayez ou vérifiez le format du prompt.")

if __name__ == "__main__":
    ingredients_utilisateur = input("Qu'as-tu dans ton frigo ? ")
    fabriquer_ma_recette(ingredients_utilisateur)