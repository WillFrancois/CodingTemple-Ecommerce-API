from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate
from flask import Flask, request, jsonify
from app import app, db

class Product(db.Model):
    __tablename__ = 'Product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False) #Integer is used for price in pennies (USD)
    description = db.Column(db.String(510), nullable=True)

class ProductSchema(Schema):
    name = fields.String(validate=validate.Length(max=255), required=True)
    price = fields.Integer(required=True, strict=True)
    description = fields.String(missing=None, validate=validate.Length(max=510), required=False)

@app.route("/product", methods=['POST'])
def add_product():
    try:
        req = request.get_json()
        product_schema = ProductSchema()
        product = ProductSchema.load(product_schema, data=req)

        product_obj = Product(name=product["name"], price=product["price"], description=product["description"])
        db.session.add(product_obj)
        db.session.commit()

        return jsonify({"message": "Success!"})

    except Exception as e:
        return jsonify({"message": f"Failure: {e}"})

@app.route("/product/<int:id>", methods=['GET'])
def get_product(id):
    try:
        products = Product.query.all()

        for product in products:
            if product.id == id:
                return jsonify({"name": product.name, "price": product.price, "description": product.description})

    except Exception as e:
        return jsonify({"message": f"Failure: {e}"})

@app.route("/product/<int:id>", methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)

    try:
        req = request.get_json()
        product_schema = ProductSchema()
        product_data = ProductSchema.load(product_schema, data=req)
        product.name = product_data["name"]
        product.price = product_data["price"]
        product.description = product_data["description"]
        db.session.commit()
        return jsonify({"message": "Success!"})

    except Exception as e:
        return jsonify({"message": f"Failure: {e}"})

@app.route("/product/<int:id>", methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)

    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Success!"})

    except Exception as e:
        return jsonify({"message": f"Failure: {e}"})

@app.route("/product/all", methods=['GET'])
def get_all_products():
    try:
        return_list = []
        products = Product.query.all()
        for product in products:
            return_list.append({"name": product.name, "price": product.price, "description": product.description})
        return return_list

    except Exception as e:
        return jsonify({"message": f"Failure: {e}"})
