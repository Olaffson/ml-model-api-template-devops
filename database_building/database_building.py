import pyodbc


def connect_to_azure_sql_server(server_name, database_name, username, password):
    """
    Se connecte à un serveur Azure SQL.

    Args:
        server_name (str): Nom du serveur Azure SQL.
        database_name (str): Nom de la base de données Azure SQL.
        username (str): Nom d'utilisateur pour la connexion.
        password (str): Mot de passe pour la connexion.

    Returns:
        pyodbc.Connection: Objet de connexion à la base de données.
    """
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={server_name}.database.windows.net,1433;"
        f"DATABASE={database_name};"
        f"UID={username};"
        f"PWD={password};"
        "Encrypt=yes;"
        # "TrustServerCertificate=no;"
        "Trusted_Connection=yes;"
        "Connection Timeout=30;"
    )
    
    conn = pyodbc.connect(conn_str)
    return conn


def execute_sql_query(connection, sql_query):
    """
    Exécute une requête SQL sur la base de données.

    Args:
        connection (pyodbc.Connection): Objet de connexion à la base de données.
        sql_query (str): Requête SQL à exécuter.

    Returns:
        None
    """
    cursor = connection.cursor()
    cursor.execute(sql_query)
    cursor.commit()
    cursor.close()


# Exemple d'utilisation
if __name__ == "__main__":
    # Informations de connexion
    server_name = "projet-ok-prod-sqlserver.database.windows.net"
    database_name = "projet-ok-prod-database"
    username = "adminlogin"
    password = "AdminPassword123!"

    # Se connecter à la base de données
    conn = connect_to_azure_sql_server(server_name, database_name, username, password)

    # Exécuter les requêtes de création de tables
    with open("create_table_prod.sql", "r") as file:
        create_table_sql = file.read()
        execute_sql_query(conn, create_table_sql)

    # Fermer la connexion
    conn.close()
