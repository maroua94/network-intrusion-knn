import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier

# Créer le dossier models/ s'il n'existe pas
if not os.path.exists('models'):
    os.makedirs('models')

# Charger le fichier
df = pd.read_csv('data/train.csv')

# Séparer X et y
X = df.drop('class', axis=1)
y = df['class']

# Identifier les colonnes catégorielles
categorical_cols = X.select_dtypes(include='object').columns.tolist()

# Créer et entraîner les encoders
encoders = {}
for col in categorical_cols:
    encoder = LabelEncoder()
    encoder.fit(X[col])
    X[col] = encoder.transform(X[col])
    encoders[col] = encoder

# Sauvegarder tous les encoders
joblib.dump(encoders, 'models/encoders.pkl')

# Diviser train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Créer et entraîner le scaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Sauvegarder le scaler
joblib.dump(scaler, 'models/scaler.pkl')

# Créer et entraîner le modèle k-NN
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)

# Calculer l'accuracy
accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy}")

# Sauvegarder le modèle
joblib.dump(model, 'models/knn_model.pkl')

print("Training completed. Models saved in models/.")