from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from base import Base

class Books(Base):
    __tablename__ ="books"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    author  = Column(String)
    year_published = Column(Integer)
    type = Column(Integer)


    def __init__(self, name, author, year_published, type):
        self.name = name
        self.author = author
        self.year_published = year_published
        self.type = type


