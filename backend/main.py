from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from pydantic import BaseModel
from models import User, Education, Training, Experience
# import datetime as dt
from datetime import datetime

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_database():
    db = None

    try:
        db = SessionLocal()
    finally:
        yield db
        db.close()

    
class UserModel(BaseModel):
    username: str
    password: str
    firstname : str
    middlename :str
    lastname :str
    email: str
    contact_no : str
    address : str


class EducationModel(BaseModel):
    school : str
    degree : str
    start_date : str
    end_date : str
    description : str
    user_id : int


class TrainingModel(BaseModel):
    training : str
    date : str
    organizer : str
    description : str
    user_id : int


class ExperienceModel(BaseModel):
    title : str
    company : str
    current_working : bool
    start_date : str
    end_date : str
    description : str
    user_id : int


@app.post('/login')
async def login(username: str, password: str, db: Session = Depends(get_database)):
    try:
        existing_user = db.query(User).filter(User.username == username).first()
        
        if existing_user:
            if existing_user.password == password:
                return { 'response': 'Login successful.', 'status_code': 200 }
            else:
                return { 'response': 'Login failed.', 'status_code': 403 }
    except:
        return { 'response': 'Login failed.', 'status_code': 403 }


@app.post('/register')
async def register(user: UserModel, db: Session = Depends(get_database)):
    try:
        existing_user = db.query(User).filter(User.username == user.username).first()

        if not existing_user:
            new_user = User()
            new_user.username = user.username
            new_user.password = user.password
            new_user.firstname = user.firstname
            new_user.middlename = user.middlename
            new_user.lastname = user.lastname
            new_user.email = user.email
            new_user.contact_no = user.contact_no
            new_user.address = user.address
            db.add(new_user)
            db.commit()

            return { 'response': 'Registration successful.', 'status_code': 200 }
        else:
            return { 'response': 'User already exists.', 'status_code': 403 }
    except:
        return { 'response': 'Registration failed.', 'status_code': 400 }


@app.post('/create_education')
async def create_education(education: EducationModel, db: Session = Depends(get_database)):
    try:
        start_date = datetime.strptime(education.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(education.end_date, "%Y-%m-%d")

        new_education = Education()
        new_education.school = education.school
        new_education.degree = education.degree
        new_education.start_date = start_date
        new_education.end_date = end_date
        new_education.description = education.description
        new_education.user_id = int(education.user_id)

        db.add(new_education)
        db.commit()
        
        return { 'response': 'Record saved sucessfully!', 'status_code': 200 }
    except:
        return { 'response': 'Failed to save record', 'status_code': 403 }


@app.post('/create_training')
async def create_training(training: TrainingModel, db: Session = Depends(get_database)):
    try:
        date = datetime.strptime(training.date, "%Y-%m-%d")

        new_training = Training()
        new_training.training = training.training
        new_training.date = date
        new_training.organizer = training.organizer
        new_training.description = training.description
        new_training.user_id = int(training.user_id)

        db.add(new_training)
        db.commit()
        
        return { 'response': 'Record saved sucessfully!', 'status_code': 200 }
    except:
        return { 'response': 'Failed to save record', 'status_code': 403 }


@app.post('/create_experience')
async def create_experience(experience: ExperienceModel, db: Session = Depends(get_database)):
    try:
        start_date = datetime.strptime(experience.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(experience.end_date, "%Y-%m-%d")

        new_experience = Experience()
        new_experience.title = experience.title
        new_experience.company = experience.company
        new_experience.current_working = experience.current_working
        new_experience.start_date = start_date
        new_experience.end_date = end_date
        new_experience.description = experience.description
        new_experience.user_id = int(experience.user_id)

        db.add(new_experience)
        db.commit()
        
        return { 'response': 'Record saved sucessfully!', 'status_code': 200 }
    except:
        return { 'response': 'Failed to save record', 'status_code': 403 }
