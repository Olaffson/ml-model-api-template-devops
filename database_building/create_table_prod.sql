-- Create table StateName
IF OBJECT_ID('StateName', 'U') IS NULL
    CREATE TABLE StateName (
        state NVARCHAR(255) PRIMARY KEY,
        state_name NVARCHAR(255)
    );
ELSE
    PRINT 'StateName exists already'


-- Create a table for Geolocation
IF OBJECT_ID('Geolocation', 'U') IS NULL
    CREATE TABLE Geolocation (
        geolocation_zip_code_prefix NVARCHAR(255) PRIMARY KEY,
        geolocation_lat FLOAT,
        geolocation_lng FLOAT,
        geolocation_city NVARCHAR(255),
        geolocation_state NVARCHAR(255),
        FOREIGN KEY (geolocation_state) REFERENCES StateName(state)
    );
ELSE
    PRINT 'Geolocation exists already'


-- Create a table for Customers
IF OBJECT_ID('Customers', 'U') IS NULL
    CREATE TABLE Customers (
    customer_id NVARCHAR(255) PRIMARY KEY,
    customer_unique_id NVARCHAR(255),
    customer_zip_code_prefix NVARCHAR(255),
    customer_city NVARCHAR(255),
    customer_state NVARCHAR(255),
    FOREIGN KEY (customer_zip_code_prefix) REFERENCES Geolocation(geolocation_zip_code_prefix)
    );
ELSE
    PRINT 'Customers exists already'


-- Create table Sellers
IF OBJECT_ID('Sellers', 'U') IS NULL
    CREATE TABLE Sellers (
        seller_id NVARCHAR(255) PRIMARY KEY,
        seller_zip_code_prefix NVARCHAR(255),
        seller_city NVARCHAR(255),
        seller_state NVARCHAR(255),
        FOREIGN KEY (seller_zip_code_prefix) REFERENCES Geolocation(geolocation_zip_code_prefix)
    );
ELSE
    PRINT 'Sellers exists already'


-- Create table Orders
IF OBJECT_ID('Orders', 'U') IS NULL
    CREATE TABLE Orders (
        order_id NVARCHAR(255) PRIMARY KEY,
        customer_id NVARCHAR(255),
        order_status NVARCHAR(255),
        order_purchase_timestamp DATETIME2,
        order_approved_at DATETIME2,
        order_delivered_carrier_date DATETIME2,
        order_delivered_customer_date DATETIME2,
        order_estimated_delivery_date DATETIME2
    );
ELSE
    PRINT 'Orders exists already'


-- Create table ProductCategoryName
IF OBJECT_ID('ProductCategoryName', 'U') IS NULL
    CREATE TABLE ProductCategoryName (
        product_category_name NVARCHAR(255) PRIMARY KEY,
        product_category_name_english NVARCHAR(255),
    );
ELSE
    PRINT 'ProductCategoryName exists already'


-- Create table Products
IF OBJECT_ID('Products', 'U') IS NULL
    CREATE TABLE Products (
        product_id NVARCHAR(255) PRIMARY KEY,
        product_category_name NVARCHAR(255),
        product_name_length INT,
        product_description_length INT,
        product_photos_qty INT,
        product_weight_g INT,
        product_length_cm INT,
        product_height_cm INT,
        product_width_cm INT,
        FOREIGN KEY (product_category_name) REFERENCES ProductCategoryName(product_category_name)
    );
ELSE
    PRINT 'Products exists already'


-- Create table OrderItem
IF OBJECT_ID('OrderItem', 'U') IS NULL
    CREATE TABLE OrderItem (
        order_id NVARCHAR(255),
        order_item_id INT,
        product_id NVARCHAR(255),
        seller_id NVARCHAR(255),
        shipping_limit_date NVARCHAR(255),
        price FLOAT,
        freight_value FLOAT,
        PRIMARY KEY (order_id, order_item_id),
        FOREIGN KEY (order_id) REFERENCES Orders(order_id),
        FOREIGN KEY (seller_id) REFERENCES Sellers(seller_id),
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    );
ELSE
    PRINT 'OrderItem exists already'
