import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

DATA_PATH = "data/network_data.csv"
MODEL_PATH = "models/knn_model.pkl"

def train_model():
    print(" Chargement du dataset :", DATA_PATH)

    # Charger dataset simple
    df = pd.read_csv(DATA_PATH)

    # Séparer X et y
    X = df[["nb_packets", "duree_connexion"]]
    y = df["etat"]   # normal ou anormal

    # Normalisation
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Modèle KNN
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X_scaled, y)

    # Sauvegarde du modèle
    os.makedirs("models", exist_ok=True)
    joblib.dump({"model": model, "scaler": scaler}, MODEL_PATH)

    print("\n Modèle SIMPLE entraîné avec succès !")
    print(" Modèle sauvegardé dans :", MODEL_PATH)

if __name__ == "__main__":
    train_model()
