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

    educations = relationship('Education', back_populates='user')
    trainings = relationship('Training', back_populates='user')
    experiences = relationship('Experience', back_populates='user')

    
class Education(Base):
    __tablename__ = 'educations'
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    school = Column(String)
    degree = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='educations')


class Training(Base):
    __tablename__ = 'trainings'
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    training = Column(String)
    date = Column(DateTime)
    organizer = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='trainings')


# For clarification
# class Achievements(Base):
#     __tablename__ = 'users'
    
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     school = Column(String)
    

class Experience(Base):
    __tablename__ = 'experiences'
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String)
    company = Column(String)
    current_working = Column(Boolean)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='experiences')


# For clarification
# class About(Base):
#     __tablename__ = 'users'
    
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     title = Column(String)


# For clarification
# class References(Base):
#     __tablename__ = 'users'
    
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     school = Column(String)
    
