from hashlib import sha256
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate
from flask import Flask, request, jsonify
from app import app, db
from customer import Customer

class CustomerAccount(db.Model):
    __tablename__ = 'CustomerAccount'
    customer = db.Column(db.Integer, db.ForeignKey("Customer.id"), nullable=False)
    username = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255))
    is_premium = db.Column(db.Boolean, nullable=False)

class CustomerAccountSchema(Schema):
    customer = fields.Integer(required=True, strict=True)
    username = fields.String(validate=validate.Length(max=255), required=True)
    password = fields.String(validate=validate.Length(max=255), required=True)
    is_premium = fields.Boolean(required=True)

@app.route("/customer_account", methods=['POST'])
def add_account():
    try:
        req = request.get_json()
        account_schema = CustomerAccountSchema()
        account = CustomerAccountSchema.load(account_schema, data=req)

        account_obj = CustomerAccount(customer=account["customer"], username=account["username"], password=str(sha256(account["password"].encode("utf-8")).hexdigest()), is_premium=account["is_premium"])
        db.session.add(account_obj)
        db.session.commit()

        return jsonify({"message": "Success!"})

    except Exception as e:
        return jsonify({"message": f"Failure: {e}"})

@app.route("/customer_account/<string:username>", methods=['GET'])
def get_account(username):
    try:
        accounts = CustomerAccount.query.all()
        customers = Customer.query.all()

        for account in accounts:
            if account.username == username:
                for customer in customers:
                    if customer.id == account.customer:
                        return jsonify({"customer_id": account.customer, "username": account.username, "password_hash": account.password, "premium": "Yes" if account.is_premium == 1 else "No", "name": customer.name, "email": customer.email, "phone_number": customer.phone_number})

    except Exception as e:
        return jsonify({"message": f"Failure: {e}"})
#
@app.route("/customer_account/<string:username>", methods=['PUT'])
def update_account(username):
    account = CustomerAccount.query.get_or_404(username)

    try:
        req = request.get_json()
        account_schema = CustomerAccountSchema()
        account_data = CustomerAccountSchema.load(account_schema, data=req)
        account.customer = account_data["customer"]
        account.username = account_data["username"]
        account.password = sha256(account_data["password"].encode("utf-8")).hexdigest()
        account.is_premium = account_data["is_premium"]
        db.session.commit()
        return jsonify({"message": "Success!"})

    except Exception as e:
        return jsonify({"message": f"Failure: {e}"})
#
@app.route("/customer_account/<string:username>", methods=['DELETE'])
def delete_account(username):
    account = CustomerAccount.query.get_or_404(username)

    try:
        db.session.delete(account)
        db.session.commit()
        return jsonify({"message": "Success!"})

    except Exception as e:
        return jsonify({"message": f"Failure: {e}"})
