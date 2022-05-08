from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from base import Base

class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    
    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age
        