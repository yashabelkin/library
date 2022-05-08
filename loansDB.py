from datetime import date
from email.policy import default
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from base import Base

class Loans(Base):
    __tablename__ = "loans"
    loan_id = Column(Integer, primary_key=True)
    cust_id = Column(Integer,ForeignKey("customers.id"))
    book_id = Column(Integer,ForeignKey("books.id"))
    loan_date = Column(String,default=date.today())
    return_date = Column(String,default=None,nullable=True)
    status = Column(String, default = 'not returned')

        
    def __init__(self, cust_id, book_id, loan_date):
        self.cust_id = cust_id
        self.book_id = book_id
        self.loan_date = loan_date
        