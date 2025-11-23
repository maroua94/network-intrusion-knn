FROM python:3.11

WORKDIR /app

# Copier tout le projet dans /app
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port (optionnel pour documentation)
EXPOSE 8000


# Commande par défaut : lancer l'API
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]