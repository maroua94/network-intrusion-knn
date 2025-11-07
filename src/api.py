from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI(title="KNN Intrusion Detection API")

# Charger le modèle
model = joblib.load("./models/knn_model.pkl")

@app.get("/")
def home():
    return {"message": "Bienvenue dans l'API de détection d'intrusion avec KNN !"}

@app.post("/predict")
def predict(nb_packets: float, duree_connexion: float):
    data = pd.DataFrame([[nb_packets, duree_connexion]], columns=["nb_packets", "duree_connexion"])
    prediction = model.predict(data)[0]
    label = "attaque" if prediction == 1 else "normal"
    return {"prediction": int(prediction), "label": label}