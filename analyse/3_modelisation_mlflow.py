import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score, accuracy_score, f1_score
import mlflow
import mlflow.onnx
from skl2onnx.common.data_types import FloatTensorType
from onnxmltools.convert import convert_sklearn

# Se connecter à la base de données SQLite
connection = sqlite3.connect("olist.db")

# Charger les données depuis la base de données
df = pd.read_sql_query("SELECT * FROM TrainingDataset", connection)
df = df.dropna()
connection.close()

# Diviser les données en ensembles d'entraînement et de test
y = df['score']
X = df[["produit_recu", "temps_livraison"]]
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)

# Entraîner le modèle
model = LogisticRegression()
model.fit(X_train, y_train)

# Évaluer le modèle
recall_train = recall_score(y_train, model.predict(X_train))
acc_train = accuracy_score(y_train, model.predict(X_train))
f1_train = f1_score(y_train, model.predict(X_train))

recall_test = recall_score(y_test, model.predict(X_test))
acc_test = accuracy_score(y_test, model.predict(X_test))
f1_test = f1_score(y_test, model.predict(X_test))

# Afficher les performances du modèle
print(f"Pour le jeu d'entraînement:\nLe recall est de {recall_train},\nL'accuracy est de {acc_train},\nLe F1 score est de {f1_train}")
print(f"Pour le jeu de test:\nLe recall est de {recall_test},\nL'accuracy est de {acc_test},\nLe F1 score est de {f1_test}")

# Convertir le modèle en format ONNX
initial_type = [('float_input', FloatTensorType([None, 2]))]
onnx_model = convert_sklearn(model, initial_types=initial_type)

# Enregistrer le modèle au format MLflow
mlflow.set_experiment("log_produitrecu")
with mlflow.start_run():
    mlflow.onnx.log_model(onnx_model, "model")
