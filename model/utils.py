import pandas as pd
import sqlite3


def lire_requete_sql(nom_fichier):
    """
    Lire le contenu d'un fichier SQL.

    Args:
        nom_fichier (str): Le chemin du fichier SQL.

    Returns:
        str: Le contenu du fichier SQL.
    """
    with open(nom_fichier, 'r') as file:
        requete = file.read()
    return requete


def executer_requete_sql(requete, nom_fichier_db):
    """
    Exécuter une requête SQL et lire les résultats dans un DataFrame.

    Args:
        requete (str): La requête SQL à exécuter.
        nom_fichier_db (str): Le chemin de la base de données SQLite.

    Returns:
        pandas.DataFrame: Le DataFrame contenant les résultats de la requête.
    """
    connection = sqlite3.connect(nom_fichier_db)
    df = pd.read_sql_query(requete, connection)
    connection.close()
    return df


def nettoyer_dataframe(df):
    """
    Nettoyer le DataFrame en supprimant certaines colonnes, en convertissant les colonnes de date et en réorganisant les colonnes.

    Args:
        df (pandas.DataFrame): Le DataFrame à nettoyer.

    Returns:
        pandas.DataFrame: Le DataFrame nettoyé.
    """
    # Supprimer les colonnes spécifiées
    colonnes_a_supprimer = ['order_estimated_delivery_date', 'order_status', 'customer_id', 'customer_unique_id']
    df.drop(columns=colonnes_a_supprimer, inplace=True)

    # Convertir les colonnes de date en format datetime
    colonnes_dates = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date']
    for colonne in colonnes_dates:
        #df[colonne] = pd.to_datetime(df[colonne], format='%Y-%m-%d %H:%M:%S')
        df[colonne] = pd.to_datetime(df[colonne])

    # Supprimer les lignes avec des valeurs manquantes
    df.dropna(inplace=True)

    # Calculer la durée de livraison (en jours)
    df['delivery_time'] = df['order_delivered_customer_date'] - df['order_purchase_timestamp']

    # Convertir la colonne delivery_time en heures
    df['delivery_time_hours'] = df['delivery_time'].dt.total_seconds() / 3600

    # Arrondir la colonne delivery_time_hours à l'entier le plus proche
    df['delivery_time_hours'] = round(df['delivery_time_hours'])

    # Convertir la colonne delivery_time_hours en entier
    df['delivery_time_hours'] = df['delivery_time_hours'].astype(int)

    # Supprimer les colonnes spécifiées
    colonnes_a_supprimer = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'delivery_time']
    df.drop(columns=colonnes_a_supprimer, inplace=True)

    # Définir l'ordre des colonnes souhaité
    nouvel_ordre_colonnes = ['order_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state', 'delivery_time_hours']
    
    # Réorganiser les colonnes
    df = df.reindex(columns=nouvel_ordre_colonnes)
    
    return df


def train_linear_regression_with_mlflow(df_reviews):
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.metrics import mean_squared_error, r2_score
    import mlflow
    import mlflow.sklearn

    features = ['customer_zip_code_prefix', 'customer_city', 'customer_state']
    target = 'delivery_time_hours'
    mlflow_tracking_uri = "http://127.0.0.1:5000"
    experiment_name = "olist_experiment"

    # Séparation des données d'entraînement et de test
    X = df_reviews[features]
    y = df_reviews[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Construction du pipeline de prétraitement
    categorical_features = ['customer_zip_code_prefix', 'customer_city', 'customer_state']
    categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])
    preprocessor = ColumnTransformer(transformers=[('cat', categorical_transformer, categorical_features)])

    # Création du pipeline complet avec le modèle de régression
    model = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', LinearRegression())])

    # Initialisation de MLflow
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    mlflow.set_experiment(experiment_name)

    # Enregistrement des paramètres et métriques avec MLflow
    with mlflow.start_run():
        # Entraînement du modèle
        model.fit(X_train, y_train)
        
        # Prédiction sur les données de test
        y_pred = model.predict(X_test)

        # Calcul des métriques
        rmse = round(mean_squared_error(y_test, y_pred, squared=False),4)
        r2 = round(r2_score(y_test, y_pred),4)
        
        # Enregistrement des métriques dans MLflow
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)

        # Enregistrement du modèle dans MLflow
        mlflow.sklearn.log_model(model, "model")
        
        # Affichage des métriques
        print("Root Mean Squared Error (RMSE):", rmse)
        print("Coefficient de détermination (R^2) sur les données de test:", r2)

