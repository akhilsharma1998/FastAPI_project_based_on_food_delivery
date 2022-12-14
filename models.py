from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(25), unique=True)
    passwored = Column(String(25), nullable=True)
    is_active = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    order = relationship('Order', back_populates='user')

    def __repr__(self):
        return f"<User {self.username}>"

class Order(Base):
    
    ORDER_STATUS=(
        ('PENDING', 'pending'),
        ('IN_TRANSIT', 'in_transit'),
        ('DELIEVERED', 'delivered')

    )

    PIZZA_SIZES=(
        ('SMALL', 'small'),
        ('MEDIUM', 'medium'),
        ('LARGE', 'large'),
        ('EXTRA-LARGE', 'extra-large')
    )

    __tablename__="orders"
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUS), default='PENDING')
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZES), default="SMALL")
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='order')


    def __repr__(self):
        return f"<Order {self.id}>"
    




