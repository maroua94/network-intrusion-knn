import pandas as pd
import joblib

# Charger les modèles et encoders
model = joblib.load('models/knn_model.pkl')
scaler = joblib.load('models/scaler.pkl')
encoders = joblib.load('models/encoders.pkl')

# Exemple d'entrée complète (toutes les colonnes sauf "class")
input_data = {
    "duration": 0,
    "protocol_type": "tcp",
    "service": "http",
    "flag": "SF",
    "src_bytes": 181,
    "dst_bytes": 5450,
    "land": 0,
    "wrong_fragment": 0,
    "urgent": 0,
    "hot": 0,
    "num_failed_logins": 0,
    "logged_in": 1,
    "num_compromised": 0,
    "root_shell": 0,
    "su_attempted": 0,
    "num_root": 0,
    "num_file_creations": 0,
    "num_shells": 0,
    "num_access_files": 0,
    "num_outbound_cmds": 0,
    "is_host_login": 0,
    "is_guest_login": 0,
    "count": 9,
    "srv_count": 9,
    "serror_rate": 0.0,
    "srv_serror_rate": 0.0,
    "rerror_rate": 0.0,
    "srv_rerror_rate": 0.0,
    "same_srv_rate": 1.0,
    "diff_srv_rate": 0.0,
    "srv_diff_host_rate": 0.0,
    "dst_host_count": 9,
    "dst_host_srv_count": 9,
    "dst_host_same_srv_rate": 1.0,
    "dst_host_diff_srv_rate": 0.0,
    "dst_host_same_src_port_rate": 1.0,
    "dst_host_srv_diff_host_rate": 0.0,
    "dst_host_serror_rate": 0.0,
    "dst_host_srv_serror_rate": 0.0,
    "dst_host_rerror_rate": 0.0,
    "dst_host_srv_rerror_rate": 0.0
}

# Transformer en DataFrame
df = pd.DataFrame([input_data])

# Appliquer les LabelEncoders pour chaque colonne catégorique
for col, encoder in encoders.items():
    df[col] = encoder.transform(df[col])

# Appliquer le StandardScaler
df_scaled = scaler.transform(df)

# Faire la prédiction
prediction = model.predict(df_scaled)

# Afficher le résultat
print("Prediction :", prediction[0])