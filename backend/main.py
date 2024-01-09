from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from pydantic import BaseModel
from models import User, JobPosting, Resume
# import datetime as dt
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class JobPostingModel(BaseModel):
    title: str
    job_title: str
    description: str
    date_posted: str
    post_status: str

class ResumeModel(BaseModel):
    resume_owner: str
    ed_1: str
    ed_2: str
    ed_3: str
    training_1: str
    training_2: str
    training_3: str
    achievement_1: str
    achievement_2: str
    achievement_3: str
    experience_1: str
    experience_2: str
    experience_3: str
    summary: str
    ref_1: str
    ref_2: str
    ref_3: str


@app.get('/show_users')
async def show_users(db: Session = Depends(get_database)):
    try:
        all_users = db.query(User).all()
        return { 'response': 'User Retrieval Success', 'users': all_users, 'status_code': 200 }
    except:
        return { 'response': 'User Retrieval Failed', 'status_code': 200 }
    

@app.post('/login')
async def login(username: str, password: str, db: Session = Depends(get_database)):
    try:
        existing_user = db.query(User).filter(User.username == username).first()
        
        if existing_user:
            if existing_user.password == password:
                return { 'response': 'Login successful.', 'user_data': existing_user, 'status_code': 200 }
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
    

@app.get('/retrieve_user_data')
async def retrieve_dashboard_data(user_id: int, db: Session = Depends(get_database)):
    try:
        user = db.query(User).filter(User.id == user_id).first()

        payload = {}
        payload.update({ 'user_data': user })

        return { 'payload': payload, 'status_code': 200 }
    except:
        return { 'response': 'Error retrieving data.', 'status_code': 400 }
    

@app.post('/create_job_posting')
async def create_job_posting(job: JobPostingModel, db: Session = Depends(get_database)):
    try:
        new_job = JobPosting()
        new_job.job_title = job.job_title
        new_job.description = job.description
        new_job.post_status = job.post_status

        db.add(new_job)
        db.commit()

        return { 'response': 'job created', 'status_code': 200 }
    except:
        return { 'response': 'Error retrieving data.', 'status_code': 400 }
    

@app.get('/show_jobs')
async def show_jobs(db: Session = Depends(get_database)):
    try:
        all_jobs = db.query(JobPosting).all()
        return { 'response': 'jobs retrieved', 'jobs': all_jobs, 'status_code': 200 }
    except:
        return { 'response': 'User Retrieval Failed', 'status_code': 200 }
    

@app.post('/apply_to_job')
async def apply_to_job(user_id: int, job_id: int, db: Session = Depends(get_database)):
    try:
        return { 'response': 'applied to job', 'status_code': 200 }
    except:
        return { 'response': 'Error retrieving data.', 'status_code': 400 }
