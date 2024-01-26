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

<<<<<<< Updated upstream
    educations = relationship('Education', back_populates='user')
    trainings = relationship('Training', back_populates='user')
    experiences = relationship('Experience', back_populates='user')
=======
    resume = relationship('Resume', back_populates='user')
    experiences = relationship('Experience', back_populates='user')
    certifications = relationship('Certification', back_populates='user')
    owner_notifs = relationship('Notification', back_populates='notif_owner')
>>>>>>> Stashed changes

    
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


<<<<<<< Updated upstream
# For clarification
# class About(Base):
#     __tablename__ = 'users'
    
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     title = Column(String)
=======
class Experience(Base):
    __tablename__ = 'experiences'

    id = Column(Integer, autoincrement=True, primary_key=True)
    job_title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship('User', back_populates='experiences')


class Certification(Base):
    __tablename__ = 'certifications'

    id = Column(Integer, autoincrement=True, primary_key=True)
    certificate_title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship('User', back_populates='certifications')


class JobApplication(Base):
    __tablename__ = 'job_applications'

    id = Column(Integer, autoincrement=True, primary_key=True)
    resume = Column(Integer, ForeignKey('resumes.id'))
    job = Column(Integer, ForeignKey('jobs.id'))

    applicant = relationship('Resume', back_populates='job_application')
    job_posting = relationship('JobPosting', back_populates='application')
>>>>>>> Stashed changes


# For clarification
# class References(Base):
#     __tablename__ = 'users'
    
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     school = Column(String)
    
