import pandas as pd
import joblib

# Charger le modèle sauvegardé
model = joblib.load("../models/model.pkl")
nouvelle_connexion = pd.DataFrame([[250, 11]], columns=["nb_packets", "duree_connexion"])

resultat = model.predict(nouvelle_connexion)
# Exemple : une connexion à tester
# [nb_packets, duree_connexion]
test_connexion = [[300, 11]]

pred = model.predict(test_connexion)

if pred[0] == 1:
    print(" Alerte : possible attaque réseau détectée !")
else:
    print("Connexion normale.")

