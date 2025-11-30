from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
import joblib
from fastapi.middleware.cors import CORSMiddleware

# Créer l'objet FastAPI
app = FastAPI()

# Ajouter CORS pour autoriser ton interface web à appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Autorise toutes les origines
    allow_credentials=True,
    allow_methods=["*"],        # Autorise POST, GET, OPTIONS...
    allow_headers=["*"],        # Autorise tous les headers
)

# Charger les modèles
model = joblib.load('models/knn_model.pkl')
scaler = joblib.load('models/scaler.pkl')
encoders = joblib.load('models/encoders.pkl')

# Créer le modèle Pydantic pour les données d'entrée
class InputData(BaseModel):
    duration: int
    protocol_type: str
    service: str
    flag: str
    src_bytes: int
    dst_bytes: int
    land: int
    wrong_fragment: int
    urgent: int
    hot: int
    num_failed_logins: int
    logged_in: int
    num_compromised: int
    root_shell: int
    su_attempted: int
    num_root: int
    num_file_creations: int
    num_shells: int
    num_access_files: int
    num_outbound_cmds: int
    is_host_login: int
    is_guest_login: int
    count: int
    srv_count: int
    serror_rate: float
    srv_serror_rate: float
    rerror_rate: float
    srv_rerror_rate: float
    same_srv_rate: float
    diff_srv_rate: float
    srv_diff_host_rate: float
    dst_host_count: int
    dst_host_srv_count: int
    dst_host_same_srv_rate: float
    dst_host_diff_srv_rate: float
    dst_host_same_src_port_rate: float
    dst_host_srv_diff_host_rate: float
    dst_host_serror_rate: float
    dst_host_srv_serror_rate: float
    dst_host_rerror_rate: float
    dst_host_srv_rerror_rate: float

def safe_transform(encoder, values):
    known = set(encoder.classes_)
    return [v if v in known else list(known)[0] for v in values]

# Route POST /predict
@app.post("/predict")
def predict(data: InputData):

    # Convertir en dictionnaire
    input_dict = data.dict()

    # Convertir en DataFrame pandas
    df = pd.DataFrame([input_dict])

    # Appliquer les LabelEncoders pour colonnes catégoriques
    for col, encoder in encoders.items():
        if col in df.columns:
            df[col] = encoder.transform(safe_transform(encoder, df[col]))

    # Appliquer le StandardScaler
    df_scaled = scaler.transform(df)

    # Faire la prédiction
    prediction = model.predict(df_scaled)[0]

    # Retourner le résultat
    return {"prediction": prediction}