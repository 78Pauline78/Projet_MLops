import mlflow

def log_recipe_event(ingredients, recipe_text):
    # Définit le nom du projet dans MLflow
    mlflow.set_experiment("Recipe_Generator")
    
    with mlflow.start_run():
        # Enregistre les ingrédients en "paramètre"
        mlflow.log_param("ingredients", ingredients)
        
        # Enregistre la recette complète en "artifact" (fichier texte)
        with open("last_recipe.txt", "w", encoding="utf-8") as f:
            f.write(recipe_text)
        mlflow.log_artifact("last_recipe.txt")
        
        print("✅ Génération enregistrée dans MLflow")