from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine=create_engine('sqlite:///library.db', echo=True, connect_args={"check_same_thread": False})
Session = sessionmaker(bind = engine)

Base = declarative_base()

