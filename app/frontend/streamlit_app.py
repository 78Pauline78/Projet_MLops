import streamlit as st
import json
import os
import re
from app.llm.recette_gen import generate_recipe 
from app.image.image_gen import generate_recipe_image
from app.pdf.pdf_builder import generer_pdf_recette
from app.tracking.mlflow_logger import log_recipe_event  # <-- Import du tracking

st.set_page_config(page_title="Le Grimoire de Grand-Mère", page_icon="🍲")

st.title("👵 Le Grimoire de Grand-Mère")
st.subheader("Entrez vos ingrédients, l'IA s'occupe du reste.")

ingredients_input = st.text_area("Qu'avez-vous dans votre frigo ?", "3 carottes, 1 oignon, du poulet")

if st.button("Générer ma recette magique ✨"):
    if ingredients_input:
        with st.spinner("La grand-mère consulte son vieux grimoire..."):
            try:
                # 1. Génération de la recette
                response = generate_recipe(ingredients_input)

                # Nettoyage et chargement du JSON
                if isinstance(response, str):
                    clean_content = re.search(r'\{.*\}', response, re.DOTALL)
                    if clean_content:
                        json_str = clean_content.group(0).replace('\n', ' ')
                        recipe_data = json.loads(json_str)
                    else:
                        recipe_data = json.loads(response)
                else:
                    recipe_data = response

                # --- TRACKING MLFLOW ---
                # On enregistre les ingrédients et le résultat JSON transformé en texte
                log_recipe_event(ingredients_input, json.dumps(recipe_data, indent=2))

                # 2. Génération de l'image
                st.info("Grand-mère prépare les fourneaux...")
                titre_recette = recipe_data.get('titre', 'Ma Recette')
                image_path = generate_recipe_image(titre_recette)

                # 3. Génération du PDF
                st.info("Écriture de la fiche recette...")
                pdf_path = generer_pdf_recette(recipe_data, image_path)

                # --- AFFICHAGE ---
                st.success("Et voilà ma recette bon appétit !")

                col1, col2 = st.columns(2)
                with col1:
                    if os.path.exists(image_path):
                        st.image(image_path, caption=titre_recette)

                with col2:
                    st.header(titre_recette)
                    st.write("**Ingrédients :**")
                    liste_propre = []
                    for ing in recipe_data.get('ingredients', []):
                        if isinstance(ing, dict):
                            nom = ing.get('nom', '')
                            quantite = ing.get('quantite', '')
                            liste_propre.append(f"{nom} ({quantite})")
                        else:
                            liste_propre.append(str(ing))
                    st.write(", ".join(liste_propre))
                    st.write("**Astuce de Grand-Mère :**")
                    st.write(recipe_data.get('astuce', 'Bon appétit !'))

                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="📥 Télécharger la fiche recette (PDF)",
                            data=f,
                            file_name="recette.pdf",
                            mime="application/pdf"
                        )

            except Exception as e:
                st.error(f"Erreur de lecture du grimoire : {e}")
                if 'response' in locals():
                    st.expander("Voir la réponse brute de l'IA").code(response)
    else:
        st.warning("Ajoute au moins un ingrédient !")
