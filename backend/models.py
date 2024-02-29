from sqlalchemy import Boolean, Column, Integer, Float, String, DateTime, ForeignKey, Date, func
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
    profile_picture = Column(String)

    resume = relationship('Resume', back_populates='user')
    owner_notifs = relationship('Notification', back_populates='notif_owner')


class JobPosting(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String)
    job_title = Column(String)
    description = Column(String)
    date_posted = Column(DateTime, server_default=func.now())
    post_status = Column(Boolean)
    date_expired = Column(DateTime)
    

    application = relationship('JobApplication', back_populates='job_posting')

class Resume(Base):
    __tablename__ = 'resumes'

    id = Column(Integer, autoincrement=True, primary_key=True)
    resume_owner = Column(Integer, ForeignKey('users.id'))
    ed_1 = Column(String)
    ed_2 = Column(String)
    ed_3 = Column(String)
    summary = Column(String)
    ref_1 = Column(String)
    ref_2 = Column(String)
    ref_3 = Column(String)

    
    user = relationship('User', back_populates='resume')
    job_application = relationship('JobApplication', back_populates='applicant')
    experiences = relationship('Experience', back_populates='resume')
    certifications = relationship('Certification', back_populates='resume')


class Experience(Base):
    __tablename__ = 'experiences'

    id = Column(Integer, autoincrement=True, primary_key=True)
    job_title = Column(String)
    company = Column(String)
    tenure_start = Column(Date)
    tenure_end = Column(Date)
    resume_id = Column(Integer, ForeignKey("resumes.id"))

    resume = relationship('Resume', back_populates='experiences')


class Certification(Base):
    __tablename__ = 'certifications'

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String)
    training_center = Column(String)
    date = Column(String)
    attachment = Column(String)
    resume_id = Column(Integer, ForeignKey("resumes.id"))

    resume = relationship('Resume', back_populates='certifications')


class JobApplication(Base):
    __tablename__ = 'job_applications'

    id = Column(Integer, autoincrement=True, primary_key=True)
    resume = Column(Integer, ForeignKey('resumes.id'))
    job = Column(Integer, ForeignKey('jobs.id'))

    applicant = relationship('Resume', back_populates='job_application')
    job_posting = relationship('JobPosting', back_populates='application')


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, autoincrement=True, primary_key=True)
    date_posted = Column(DateTime, server_default=func.now())
    message = Column(String)
    sent_to = Column(Integer, ForeignKey('users.id'))

    notif_owner = relationship('User', back_populates='owner_notifs')

