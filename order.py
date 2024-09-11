from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from product import Product
from customer import Customer

from app import app, db

class Order(db.Model):
    __tablename__ = 'Order'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("Product.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("Customer.id"), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    delivery_instructions = db.Column(db.String(510), nullable=True)
    order_status = db.Column(db.String(100), nullable=False)

class OrderSchema(Schema):
    p_id = fields.Integer(required=True, strict=True)
    c_id = fields.Integer(required=True, strict=True)
    address = fields.String(validate=validate.Length(max=255), required=True)
    instructions = fields.String(missing=None, validate=validate.Length(max=510), required=False)

@app.route("/order", methods=['POST'])
def add_order():
    try:
        req = request.get_json()
        order_schema = OrderSchema()
        order = OrderSchema.load(order_schema, data=req)

        order_obj = Order(product_id=order["p_id"], customer_id=order["c_id"], order_date=datetime.now(), address=order["address"], delivery_instructions=order["instructions"], order_status="Ordered")
        db.session.add(order_obj)
        db.session.commit()

        return jsonify({"message": "Success!"})

    except Exception as e:
        return jsonify({"message": f"Failure: {e}"})

@app.route("/order/<int:id>", methods=['GET'])
def get_order(id):
    order = Order.query.get_or_404(id)
    product = Product.query.get_or_404(order.product_id)
    customer = Customer.query.get_or_404(order.customer_id)

    try:
        return jsonify({"customer name": customer.name, "product name": product.name, "order date": order.order_date, "address": order.address, "instructions": order.delivery_instructions, "status": order.order_status})

    except Exception as e:
        return jsonify({"message": f"Failure: {e}"})

@app.route("/order/track/<int:id>", methods=['GET'])
def track_order(id):
    order = Order.query.get_or_404(id)

    try:
        return jsonify({"order date": order.order_date, "expected date": order.order_date + timedelta(days=7), "status": order.order_status})

    except Exception as e:
        return jsonify({"message": f"Failure: {e}"})
