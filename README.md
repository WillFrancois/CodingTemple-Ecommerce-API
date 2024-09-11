# E-Commerce API
This repository contains files for an E-Commerce API that runs using GET, POST, PUT, and DELETE requests and provides JSON responses. Information can be stored through a MySQL database (default database name is ecommerce_app with the password 'my-secret-pw').

To run the application, create a local database with the name ecommerce_app. Then provide the command "./env/bin/flask run" in the root of this repository's folder.

The libraries used include flask, flask-marshmallow, flask-sqlalchemy, as well as files from the standard library such as hashlib and datetime.

## Files included

### App.py
The main file that runs the application and provides tables for the database to create on startup.

### Customer.py
Contains the Customer class and schema as well as routes to provide API functionality for the Customer table in MySQL. Customer API calls use the "/customer" route location for receiving JSON.

### Customer_account.py
Contains the CustomerAccount class and schema as well as routes to provide API functionality for the CustomerAccount table in MySQL. Customer account API calls use the "/customer_account" route location for receiving JSON.

### Order.py
Contains the Order class and schema as well as routes to provide API functionality for the Order table in MySQL. (To query from within MySQL, use backticks around the word Order. i.e. \`Order\`). Order API calls use the "/order" route location for receiving JSON.

### Product.py
Contains the Product class and schema as well as routes to provide API functionality for the Product table in MySQL. Product API calls use the "/product" route location for receiving JSON.

### E-commerce API.postman_collection.json
Provides sample input for the routes that are created in the files listed above. Input and output is sent as JSON.
