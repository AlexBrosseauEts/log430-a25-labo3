"""
Product (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from db import get_sqlalchemy_session
from stocks.models.product import Product
from stocks.models.stock import Stock

def get_stock_by_id(product_id):
    """Get stock by product ID """
    session = get_sqlalchemy_session()
    result = session.query(Stock).filter_by(product_id=product_id).all()
    if len(result):
        return {
            'product_id': result[0].product_id,
            'quantity': result[0].quantity,
        }
    else:
        return {}

def get_stock_for_all_products():
    """Get stock quantity for all products, joined with Product info, as a list of dicts"""
    session = get_sqlalchemy_session()
    try:
        rows = (
            session.query(
                Stock.product_id.label("product_id"),
                Stock.quantity.label("quantity"),
                Product.name.label("name"),
                Product.sku.label("sku"),
                Product.price.label("price"),
            )
            .join(Product, Product.id == Stock.product_id)
            .all()
        )

        # SQLALCH to json type
        return [
            {
                "product_id": int(r.product_id),
                "quantity": int(r.quantity),
                "name": r.name,
                "sku": r.sku,
                "price": float(r.price),
            }
            for r in rows
        ]
    finally:
        return {}
