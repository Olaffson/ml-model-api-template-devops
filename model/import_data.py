from utils import lire_requete_sql, executer_requete_sql, nettoyer_dataframe, train_linear_regression_with_mlflow
import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import pandas as pd


# Chemin vers le fichier de requête SQL
chemin_requete_sql = '../sql_queries/request_model.sql'


# Connexion à la base de données et exécution de la requête
df_reviews = executer_requete_sql(lire_requete_sql(chemin_requete_sql), "../olist.db")


# Netoyage du DataFrame df_reviews
df_reviews = nettoyer_dataframe(df_reviews)


# Entrainer le model
train_linear_regression_with_mlflow(df_reviews)
