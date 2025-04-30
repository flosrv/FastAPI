from sqlmodel import Session, select
from typing import List, Optional
from .models import User, Product, Order, OrderItem

# Create a new user
def create_user(session: Session, username: str, email: str) -> User:
    user = User(username=username, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Get a user by ID
def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)

# Update user details
def update_user(session: Session, user_id: int, username: Optional[str] = None, email: Optional[str] = None) -> Optional[User]:
    user = session.get(User, user_id)
    if user:
        if username:
            user.username = username
        if email:
            user.email = email
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

# Delete a user
def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
        return True
    return False

# Create a new product
def create_product(session: Session, name: str, price: float, stock: int) -> Product:
    product = Product(name=name, price=price, stock=stock)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

# Get a product by ID
def get_product_by_id(session: Session, product_id: int) -> Optional[Product]:
    return session.get(Product, product_id)

# Update product details
def update_product(session: Session, product_id: int, name: Optional[str] = None, price: Optional[float] = None, stock: Optional[int] = None) -> Optional[Product]:
    product = session.get(Product, product_id)
    if product:
        if name:
            product.name = name
        if price:
            product.price = price
        if stock is not None:
            product.stock = stock
        session.add(product)
        session.commit()
        session.refresh(product)
    return product

# Delete a product
def delete_product(session: Session, product_id: int) -> bool:
    product = session.get(Product, product_id)
    if product:
        session.delete(product)
        session.commit()
        return True
    return False

# Create a new order
def create_order(session: Session, user_id: int, items: List[dict]) -> Order:
    order = Order(user_id=user_id)
    session.add(order)
    session.commit()
    session.refresh(order)
    for item in items:
        order_item = OrderItem(order_id=order.id, product_id=item["product_id"], quantity=item["quantity"])
        session.add(order_item)
    session.commit()
    return order

# Get an order by ID
def get_order_by_id(session: Session, order_id: int) -> Optional[Order]:
    return session.get(Order, order_id)

# Get all orders for a user
def get_orders_by_user(session: Session, user_id: int) -> List[Order]:
    return session.exec(select(Order).where(Order.user_id == user_id)).all()

# Update order status
def update_order_status(session: Session, order_id: int, status: str) -> Optional[Order]:
    order = session.get(Order, order_id)
    if order:
        order.status = status
        session.add(order)
        session.commit()
        session.refresh(order)
    return order

# Delete an order
def delete_order(session: Session, order_id: int) -> bool:
    order = session.get(Order, order_id)
    if order:
        session.delete(order)
        session.commit()
        return True
    return False

# Get inventory levels
def get_inventory_levels(session: Session) -> List[Product]:
    return session.exec(select(Product)).all()

# Update inventory stock
def update_inventory_stock(session: Session, product_id: int, stock: int) -> Optional[Product]:
    product = session.get(Product, product_id)
    if product:
        product.stock = stock
        session.add(product)
        session.commit()
        session.refresh(product)
    return product

# Get low-stock products
def get_low_stock_products(session: Session, threshold: int) -> List[Product]:
    return session.exec(select(Product).where(Product.stock < threshold)).all()

# Get order details with items
def get_order_details(session: Session, order_id: int) -> Optional[Order]:
    return session.exec(select(Order).where(Order.id == order_id).options(selectinload(Order.items))).first()

# Bulk create products
def bulk_create_products(session: Session, products: List[Product]) -> List[Product]:
    session.add_all(products)
    session.commit()
    return products

# Bulk update product prices
def bulk_update_product_prices(session: Session, updates: List[dict]) -> List[Product]:
    updated_products = []
    for update in updates:
        product = session.get(Product, update["id"])
        if product:
            product.price = update["price"]
            session.add(product)
            updated_products.append(product)
    session.commit()
    return updated_products

# Delete all orders for a user
def delete_all_orders_for_user(session: Session, user_id: int) -> None:
    session.exec(select(Order).where(Order.user_id == user_id).delete())
    session.commit()

# Get revenue by product
def get_revenue_by_product(session: Session) -> List[dict]:
    result = session.exec(
        select(Product.name, (OrderItem.quantity * Product.price).label("revenue"))
        .join(OrderItem, Product.id == OrderItem.product_id)
        .group_by(Product.name)
    ).all()
    return [{"product": row[0], "revenue": row[1]} for row in result]
