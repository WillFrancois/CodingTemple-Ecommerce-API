from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate
from flask import Flask, request, jsonify

from app import app, db

class Customer(db.Model):
    __tablename__ = 'Customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

class CustomerSchema(Schema):
    name = fields.String(validate=validate.Length(max=255), required=True)
    email = fields.String(validate=validate.Length(max=255), required=True)
    phone_number = fields.String(validate=validate.Length(max=20), required=True)

@app.route("/customer", methods=['POST'])
def add_customer():
    try:
        req = request.get_json()
        customer_schema = CustomerSchema()
        customer = CustomerSchema.load(customer_schema, data=req)

        customer_obj = Customer(name=customer["name"], email=customer["email"], phone_number=customer["phone_number"])
        db.session.add(customer_obj)
        db.session.commit()

        return jsonify({"message": "Success!"})

    except Exception as e:
        return jsonify({"message": f"Failure: {e}"})

@app.route("/customer/<int:id>", methods=['GET'])
def get_customer(id):
    try:
        customers = Customer.query.all()

        for customer in customers:
            if customer.id == id:
                return jsonify({"name": customer.name, "email": customer.email, "phone number": customer.phone_number})

    except Exception as e:
        return jsonify({"message": f"Failure: {e}"})

@app.route("/customer/<int:id>", methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)

    try:
        req = request.get_json()
        customer_schema = CustomerSchema()
        customer_data = CustomerSchema.load(customer_schema, data=req)
        customer.name = customer_data["name"]
        customer.email = customer_data["email"]
        customer.phone_number = customer_data["phone_number"]
        db.session.commit()
        return jsonify({"message": "Success!"})

    except Exception as e:
        return jsonify({"message": f"Failure: {e}"})

@app.route("/customer/<int:id>", methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)

    try:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": "Success!"})

    except Exception as e:
        return jsonify({"message": f"Failure: {e}"})
