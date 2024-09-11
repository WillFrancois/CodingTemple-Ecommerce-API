from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:my-secret-pw@localhost/ecommerce_app'
db = SQLAlchemy(app)

# Imports must occur after the Flask app is created to pass a
# reference to the namespaces
import customer
import customer_account
import product
import order

with app.app_context():
    db.create_all()
