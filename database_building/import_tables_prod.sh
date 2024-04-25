# # Azure SQL Server credentials
# server="projet-ok-prod-sqlserver.database.windows.net"
# database="projet-ok-prod-database"
# username="adminlogin"
# password="AdminPassword123!"

 
# # Path to your CSV file
# csvFileOrders="/home/utilisateur/Documents/Projets/modele_API_Charles/ml-model-api-template-devops/data/state_name.csv"

# # Import data
# bcp StateName in $csvFileOrders -S $server -d $database -U $username -P $password -q -c -t ","

 
# # Path to your CSV file
# csvFileOrders="/home/utilisateur/Documents/Projets/modele_API_Charles/ml-model-api-template-devops/data/geolocation_dataset.csv"

# # Import data
# bcp Geolocation in $csvFileOrders -S $server -d $database -U $username -P $password -q -c -t ","

 
# # Path to your CSV file
# csvFileOrders="/home/utilisateur/Documents/Projets/modele_API_Charles/ml-model-api-template-devops/data/customers_dataset.csv"

# # Import data
# bcp Customers in $csvFileOrders -S $server -d $database -U $username -P $password -q -c -t ","

 
# # Path to your CSV file
# csvFileOrders="/home/utilisateur/Documents/Projets/modele_API_Charles/ml-model-api-template-devops/data/sellers_dataset.csv"

# # Import data
# bcp Sellers in $csvFileOrders -S $server -d $database -U $username -P $password -q -c -t ","


# # Path to your CSV file
# csvFileOrders="/home/utilisateur/Documents/Projets/modele_API_Charles/ml-model-api-template-devops/data/orders_dataset.csv"

# # Import data
# bcp Orders in $csvFileOrders -S $server -d $database -U $username -P $password -q -c -t ","


# # Path to your CSV file
# csvFileReviews="/home/utilisateur/Documents/Projets/modele_API_Charles/ml-model-api-template-devops/data/olist_order_reviews_dataset.csv"

# # Import data
# bcp Reviews in $csvFileReviews -S $server -d $database -U $username -P $password -q -c -t ","

 
# # Path to your CSV file
# csvFileReviews="/home/utilisateur/Documents/Projets/modele_API_Charles/ml-model-api-template-devops/data/product_category_name_translation.csv"

# # Import data
# bcp ProductCategoryName in $csvFileReviews -S $server -d $database -U $username -P $password -q -c -t ","

 
# # Path to your CSV file
# csvFileReviews="/home/utilisateur/Documents/Projets/modele_API_Charles/ml-model-api-template-devops/data/products_dataset.csv"

# # Import data
# bcp Products in $csvFileReviews -S $server -d $database -U $username -P $password -q -c -t ","

 
# # Path to your CSV file
# csvFileReviews="/home/utilisateur/Documents/Projets/modele_API_Charles/ml-model-api-template-devops/data/order_items_dataset.csv"

# # Import data
# bcp OrderItem in $csvFileReviews -S $server -d $database -U $username -P $password -q -c -t ","

#####################################################################################################################


# Azure SQL Server credentials
server=$AZURE_SQL_SERVER
database=$AZURE_SQL_DATABASE
username=$AZURE_SQL_USERNAME
password=$AZURE_SQL_PASSWORD

# Function to import data into a table if it doesn't exist already
import_data() {
    local table_name="$1"
    local csv_file="$2"
    local check_query="SELECT TOP 1 1 FROM $table_name"

    if sqlcmd -S $server -d $database -U $username -P $password -Q "$check_query" | grep -q 1; then
        echo "Data already exists in $table_name table."
    else
        if bcp $table_name in $csv_file -S $server -d $database -U $username -P $password -q -c -t ","; then
            echo "Data imported successfully into $table_name table."
        else
            echo "Failed to import data into $table_name table."
        fi
    fi
}

# Path to your CSV files
csvFiles=(
    "/home/utilisateur/Documents/Projets/modele_API_Charles/ml-model-api-template-devops/data/state_name.csv"
    "/home/utilisateur/Documents/Projets/modele_API_Charles/ml-model-api-template-devops/data/geolocation_dataset.csv"
    "/home/utilisateur/Documents/Projets/modele_API_Charles/ml-model-api-template-devops/data/customers_dataset.csv"
    "/home/utilisateur/Documents/Projets/modele_API_Charles/ml-model-api-template-devops/data/sellers_dataset.csv"
    "/home/utilisateur/Documents/Projets/modele_API_Charles/ml-model-api-template-devops/data/orders_dataset.csv"
    "/home/utilisateur/Documents/Projets/modele_API_Charles/ml-model-api-template-devops/data/olist_order_reviews_dataset.csv"
    "/home/utilisateur/Documents/Projets/modele_API_Charles/ml-model-api-template-devops/data/product_category_name_translation.csv"
    "/home/utilisateur/Documents/Projets/modele_API_Charles/ml-model-api-template-devops/data/products_dataset.csv"
    "/home/utilisateur/Documents/Projets/modele_API_Charles/ml-model-api-template-devops/data/order_items_dataset.csv"
)

# Import data into each table
for csvFile in "${csvFiles[@]}"; do
    table_name=$(basename "$csvFile" | cut -d '.' -f 1)
    import_data "$table_name" "$csvFile"
done
