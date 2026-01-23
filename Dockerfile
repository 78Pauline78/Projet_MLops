# Utilise une image Python officielle comme base
FROM python:3.10-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie le fichier des dépendances Python
COPY requirements.txt ./

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code de l'application dans le répertoire de travail
COPY . .

# Expose le port sur lequel Streamlit va tourner
EXPOSE 8501

# Commande pour lancer l'application Streamlit au démarrage du conteneur
# Utilise 'python -m streamlit run' pour mieux gérer les imports
CMD ["python", "-m", "streamlit", "run", "app/frontend/streamlit_app.py"]
