from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI(title="KNN Intrusion Detection API")

# Charger modèle + scaler
data = joblib.load("./models/knn_model.pkl")
model = data["model"]
scaler = data["scaler"]

@app.get("/")
def home():
    return {"message": "Bienvenue dans l'API de détection d'intrusion avec KNN !"}

@app.post("/predict")
def predict(nb_packets: float, duree_connexion: float):

    # Préparer les données
    X = pd.DataFrame([{
        "nb_packets": float(nb_packets),
        "duree_connexion": float(duree_connexion)
    }])

    # Normaliser
    X_scaled = scaler.transform(X)

    # Prédiction (numpy.int64 ou numpy.str)
    pred = model.predict(X_scaled)[0]

    # Convertir numpy -> string simple
    pred = str(pred)

    return {
        "prediction": pred,
        "label": pred
    }
