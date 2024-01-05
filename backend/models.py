from sqlalchemy import Boolean, Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String)
    password = Column(String)
    firstname = Column(String)
    middlename = Column(String)
    lastname = Column(String)
    email = Column(String)
    contact_no = Column(String)
    address = Column(String)
    user_type = Column(Boolean)
