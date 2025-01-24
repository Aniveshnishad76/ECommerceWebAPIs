from src.schema.schema implement ProductModel, CategoryModel, OrderModel

db = get_db()

def create_obj(payload):
    """Obj creation for product model"""

    obj = ProductModel.validate_model(payload)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def read_obj(obj_id):
    """read product with id"""

    return db.query(ProductModel).filter(obj.id=obj_id).first()

def update_product(obj_id, payload):
    """Update product obj with update or patch request"""

    product = db.query(ProductModel).filter(obj.id=obj_id).first()
    product.name = payload.name
    product.description = payload.description
    product.price = payload.price
    product.stock = payload.stock
    db.commit()
    db.refresh(product)
    return product

def read_all_products(db):
    """read all products"""

    return db.query(ProductModel).all()

def create_category_obj(payload):
    """Obj creation for product model"""

    obj = CategoryModel.validate_model(payload)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def create_category_obj(payload):
    """Obj creation for product model"""

    obj = CategoryModel.validate_model(payload)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def read_all_category(db):
    """read all categories"""

    return db.query(CategoryModel).all()

def read_all_orders(db):
    """read all orders"""

    return db.query(OrderModel).all()
