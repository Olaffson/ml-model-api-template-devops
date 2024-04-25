#!/bin/bash


# Azure SQL Server credentials
server=$AZURE_SQL_SERVER
database=$AZURE_SQL_DATABASE
username=$AZURE_SQL_USERNAME
password=$AZURE_SQL_PASSWORD

# Path to your SQL script file
sqlScript="/home/utilisateur/Documents/Projets/modele API Charles/ml-model-api-template-devops/database_building/create_table_prod.sql"

# Connect to Azure SQL Server and execute the SQL script
sqlcmd -S $server -d $database -U $username -P $password -i "$sqlScript"