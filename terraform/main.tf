provider "azurerm" {
  features {}
}

# Création d'un groupe de ressource
resource "azurerm_resource_group" "projet-rg" {
  name     = "projet-ok-prod-rg"
  location = "francecentral"
}

# Création d'un plan de service
resource "azurerm_app_service_plan" "projet-pas" {
  name                = "projet-ok-prod-pas"
  location            = azurerm_resource_group.projet-rg.location
  resource_group_name = azurerm_resource_group.projet-rg.name

  sku {
    tier = "Free"
    size = "F1"
  }
}

# # Création d'un registre de conteneur
# resource "azurerm_container_registry" "projet_acr" {
#   name                     = "projet-ok-prod-container"
#   resource_group_name      = azurerm_resource_group.projet-rg.name
#   location                 = azurerm_resource_group.projet-rg.location
#   sku                      = "Basic"
#   admin_enabled            = false
#   public_network_access_enabled = true
#   zone_redundancy_enabled  = false
# }

# Création d'un serveur SQL
resource "azurerm_sql_server" "projet-sqlserveur" {
  name                         = "projet-ok-prod-sqlserver"
  resource_group_name          = azurerm_resource_group.projet-rg.name
  location                     = azurerm_resource_group.projet-rg.location
  version                      = "12.0"
  administrator_login          = "adminlogin"
  administrator_login_password = "AdminPassword123!"
}

# Création d'une base de données sur le serveur SQL
resource "azurerm_sql_database" "projet-database" {
  name                = "projet-ok-prod-database"
  resource_group_name = azurerm_resource_group.projet-rg.name
  location            = azurerm_resource_group.projet-rg.location
  server_name         = azurerm_sql_server.projet-sqlserveur.name
  edition             = "Basic"
  collation           = "SQL_Latin1_General_CP1_CI_AS"
  max_size_gb         = 1
  
}

resource "azurerm_sql_firewall_rule" "allow_client_ip" {
  name                = "AllowClientIP"
  resource_group_name = azurerm_resource_group.projet-rg.name
  server_name         = azurerm_sql_server.projet-sqlserveur.name
  start_ip_address    = "212.114.17.77"
  end_ip_address      = "212.114.17.77"
}

