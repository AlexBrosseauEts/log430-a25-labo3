import graphene
from graphene import ObjectType, String, Int
from stocks.schemas.product import Product
from db import get_redis_conn

class Query(ObjectType):       
    product = graphene.Field(Product, id=String(required=True))
    stock_level = Int(product_id=String(required=True))
    
    r = get_redis_conn()
        d = r.hgetall(f"stock:{id}")
        if d:
            return Product(
                id=int(id),
                name=d.get("name") or f"Product {id}",
                sku=d.get("sku") or "",
                price=float(d.get("price")) if d.get("price") else 0.0,
                quantity=int(d.get("quantity") or 0),
            )
        return None

    
    def resolve_stock_level(self, info, product_id):
        """ Retrieve stock quantity from Redis """
        redis_client = get_redis_conn()
        quantity = redis_client.hget(f"stock:{product_id}", "quantity")
        return int(quantity) if quantity else 0