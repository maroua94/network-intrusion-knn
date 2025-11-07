import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

# --- Fonction principale d'entraînement ---
def train_model():
    print("🚀 Début de l'entraînement du modèle KNN...")

    # Charger les données
    data_path = "data/network_data.csv"
    data = pd.read_csv(data_path)

    # Suppose que le dataset a une colonne 'label' pour la classe
    X = data.drop("label", axis=1)
    y = data["label"]

    # Séparation des données
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Création et entraînement du modèle KNN
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X_train, y_train)

    # Évaluation
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Entraînement terminé — Précision: {acc*100:.2f}%")

    # Sauvegarde du modèle
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/knn_model.pkl")
    print("💾 Modèle enregistré dans models/knn_model.pkl")

if __name__ == "__main__":
    train_model()
