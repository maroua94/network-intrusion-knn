import os
import time
import hashlib
from train import train_model  # tu appelles ton script d’entraînement

DATA_PATH = "data/network_data.csv"
MODEL_PATH = "models/knn_model.pkl"
HASH_PATH = "models/last_hash.txt"

def get_file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def main():
    last_hash = None
    if os.path.exists(HASH_PATH):
        with open(HASH_PATH, "r") as f:
            last_hash = f.read()

    current_hash = get_file_hash(DATA_PATH)

    if current_hash != last_hash:
        print(" Dataset changé → réentraînement du modèle...")
        train_model()
        with open(HASH_PATH, "w") as f:
            f.write(current_hash)
        print(" Modèle mis à jour.")
    else:
        print(" Aucun changement détecté dans le dataset.")

if __name__ == "__main__":
    main()
