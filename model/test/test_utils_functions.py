
import pytest
import sqlite3
import pandas as pd
from unittest.mock import patch
from utils import lire_requete_sql, executer_requete_sql, nettoyer_dataframe, train_linear_regression_with_mlflow
from sklearn.metrics import mean_squared_error, r2_score, f1_score, accuracy_score
from sklearn.model_selection import train_test_split


TEST_DB_PATH = 'test.db'


@pytest.fixture(scope='session')
def setup_test_database():
    connection = sqlite3.connect(TEST_DB_PATH)
    yield connection
    connection.close()


def test_executer_requete_sql(setup_test_database):
    # Mocking the database with sample data
    with patch('utils.pd.read_sql_query') as mock_read_sql_query:
        mock_read_sql_query.return_value = pd.DataFrame({
            'order_id': [1, 2, 3],
            'customer_zip_code_prefix': [12345, 67890, 54321],
            'customer_city': ['City1', 'City2', 'City3'],
            'customer_state': ['State1', 'State2', 'State3']
        })

        # Call the function to be tested
        df = executer_requete_sql('SELECT * FROM Orders', TEST_DB_PATH)

        # Check if the function returns the expected DataFrame
        assert len(df) == 3


def test_nettoyer_dataframe():
    # Create a DataFrame with sample data including the columns to be dropped
    df = pd.DataFrame({
        'order_id': [1, 2, 3],
        'customer_zip_code_prefix': [12345, 67890, 54321],
        'customer_city': ['City1', 'City2', 'City3'],
        'customer_state': ['State1', 'State2', 'State3'],
        'order_purchase_timestamp': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'order_approved_at': ['2024-01-05', '2024-01-06', '2024-01-07'],
        'order_delivered_carrier_date': ['2024-01-08', '2024-01-09', '2024-01-10'],
        'order_delivered_customer_date': ['2024-01-10', '2024-01-15', '2024-01-20'],
        'order_estimated_delivery_date': ['2024-01-15', '2024-01-20', '2024-01-25'],
        'order_status': ['Delivered', 'Delivered', 'Delivered'],
        'customer_id': [1001, 1002, 1003],
        'customer_unique_id': ['unique1', 'unique2', 'unique3']
    })
    
    # Call the function to be tested
    df_cleaned = nettoyer_dataframe(df)
    
    # Check if the DataFrame is cleaned as expected
    assert len(df_cleaned) == 3
    assert 'order_purchase_timestamp' not in df_cleaned.columns
    assert 'order_delivered_customer_date' not in df_cleaned.columns
    assert 'order_estimated_delivery_date' not in df_cleaned.columns
    assert 'order_status' not in df_cleaned.columns
    assert 'customer_id' not in df_cleaned.columns
    assert 'customer_unique_id' not in df_cleaned.columns


@pytest.fixture
def df_reviews():
    # Créer un DataFrame fictif pour les tests
    df = pd.DataFrame({
        'customer_zip_code_prefix': [12345, 67890, 54321],
        'customer_city': ['City1', 'City2', 'City3'],
        'customer_state': ['State1', 'State2', 'State3'],
        'delivery_time_hours': [10, 20, 30]
    })
    return df


def test_train_linear_regression_with_mlflow(df_reviews):
    from sklearn.linear_model import LinearRegression

    # Appel de la fonction à tester
    run_id, model, rmse, r2 = train_linear_regression_with_mlflow(df_reviews)

    # Vérifier si un run ID est retourné
    assert isinstance(run_id, str)
    assert len(run_id) > 0  # S'assurer qu'un ID valide est retourné

    # Vérifier le type de modèle retourné
    assert isinstance(model, LinearRegression)

    # Vérifier que les métriques RMSE et R2 sont calculées correctement
    assert isinstance(rmse, float)
    assert isinstance(r2, float)

    # Vérifier que les métriques sont dans des plages raisonnables
    assert rmse >= 0
    assert r2 >= 0 and r2 <= 1
