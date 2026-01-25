import mlflow
import json
import os

def log_recipe_details(ingredients, recipe_data, image_path=None, pdf_path=None):
    """Logs details of a single recipe generation event."""
    # Assure-toi que le nom de l'expérience est défini
    mlflow.set_experiment("Recipe_Generator")

    with mlflow.start_run():
        # Log paramètres
        mlflow.log_param("ingredients_input", ingredients)
        mlflow.log_param("recipe_title", recipe_data.get('titre', ''))
        mlflow.log_param("prep_time", recipe_data.get('temps_preparation', '')) # Adapte

        # Log artifacts
        mlflow.log_text(json.dumps(recipe_data, indent=2), "recipe_output.json")
        if image_path and os.path.exists(image_path):
            mlflow.log_artifact(image_path, "generated_image")
        if pdf_path and os.path.exists(pdf_path):
            mlflow.log_artifact(pdf_path, "generated_pdf")
        
        print("✅ Détails de la recette enregistrés dans MLflow.")
