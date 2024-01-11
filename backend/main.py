from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from pydantic import BaseModel
from models import User, JobPosting, Resume, JobApplication
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
    post_status: bool

class ResumeModel(BaseModel):
    resume_owner: int
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

            newly_added = db.query(User).filter(User.username == user.username).first()

            new_resume = Resume()
            new_resume.resume_owner = newly_added.id
            new_resume.ed_1 = ''
            new_resume.ed_2 = ''
            new_resume.ed_3 = ''
            new_resume.training_1 = ''
            new_resume.training_2 = ''
            new_resume.training_3 = ''
            new_resume.achievement_1 = ''
            new_resume.achievement_2 = ''
            new_resume.achievement_3 = ''
            new_resume.experience_1 = ''
            new_resume.experience_2 = ''
            new_resume.experience_3 = ''
            new_resume.summary = ''
            new_resume.ref_1 = ''
            new_resume.ref_2 = ''
            new_resume.ref_3 = ''
            db.add(new_resume)
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
    

@app.post('/submit_resume')
async def submit_resume(resume: ResumeModel, db: Session = Depends(get_database)):
    try:
        existing_resume = db.query(Resume).filter(Resume.resume_owner == resume.resume_owner).first()

        if not existing_resume:
            new_resume = Resume()
            new_resume.resume_owner = resume.resume_owner
            new_resume.ed_1 = resume.ed_1
            new_resume.ed_2 = resume.ed_2
            new_resume.ed_3 = resume.ed_3
            new_resume.training_1 = resume.training_1
            new_resume.training_2 = resume.training_2
            new_resume.training_3 = resume.training_3
            new_resume.achievement_1 = resume.achievement_1
            new_resume.achievement_2 = resume.achievement_2
            new_resume.achievement_3 = resume.achievement_3
            new_resume.experience_1 = resume.experience_1
            new_resume.experience_2 = resume.experience_2
            new_resume.experience_3 = resume.experience_3
            new_resume.summary = resume.summary
            new_resume.ref_1 = resume.ref_1
            new_resume.ref_2 = resume.ref_2
            new_resume.ref_3 = resume.ref_3

            db.add(new_resume)
        else:
            existing_resume.resume_owner = resume.resume_owner
            existing_resume.ed_1 = resume.ed_1
            existing_resume.ed_2 = resume.ed_2
            existing_resume.ed_3 = resume.ed_3
            existing_resume.training_1 = resume.training_1
            existing_resume.training_2 = resume.training_2
            existing_resume.training_3 = resume.training_3
            existing_resume.achievement_1 = resume.achievement_1
            existing_resume.achievement_2 = resume.achievement_2
            existing_resume.achievement_3 = resume.achievement_3
            existing_resume.experience_1 = resume.experience_1
            existing_resume.experience_2 = resume.experience_2
            existing_resume.experience_3 = resume.experience_3
            existing_resume.summary = resume.summary
            existing_resume.ref_1 = resume.ref_1
            existing_resume.ref_2 = resume.ref_2
            existing_resume.ref_3 = resume.ref_3
            
        db.commit()

        return { 'response': 'resume submitted', 'status_code': 200 }
    except:
        return { 'response': 'Error retrieving data.', 'status_code': 400 }


@app.get('/show_resumes')
async def show_resumes(db: Session = Depends(get_database)):
    try:
        all_resumes = db.query(Resume).all()
        return { 'response': 'resumes retrieved', 'resumes': all_resumes, 'status_code': 200 }
    except:
        return { 'response': 'resumes Retrieval Failed', 'status_code': 200 }
    

@app.get('/retrieve_resume_data')
async def retrieve_resume_data(user_id: int, db: Session = Depends(get_database)):
    try:
        resume = db.query(Resume).filter(Resume.resume_owner == user_id).first()
        return { 'response': 'resume retrieved', 'resume': resume, 'status_code': 200 }
    except:
        return { 'response': 'resume Retrieval Failed', 'status_code': 200 }


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
        job_id = db.query(JobPosting).filter(JobPosting.id == job_id).first()
        resume = db.query(Resume).filter(Resume.resume_owner == user_id).first()

        new_application = JobApplication()
        new_application.resume = resume.id
        new_application.job = job_id.id

        db.add(new_application)
        db.commit()
        return { 'response': 'applied to job', 'status_code': 200 }
    except:
        return { 'response': 'Error retrieving data.', 'status_code': 400 }


@app.get('/show_applications')
async def show_applications(db: Session = Depends(get_database)):
    try:
        all_applications = db.query(JobApplication).all()
        return { 'response': 'applications retrieved', 'applications': all_applications, 'status_code': 200 }
    except:
        return { 'response': 'applications Retrieval Failed', 'status_code': 200 }
    

@app.get('/analyze_resumes')
async def analyze_resumes(job_id: int, db: Session = Depends(get_database)):
    # try:
        job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
        all_applications = db.query(JobApplication).filter(JobApplication.job == job_id).all()

        top_applicants = []

        for application in all_applications:
            resume = db.query(Resume).join(User).filter(Resume.id == application.resume).filter(User.id == Resume.resume_owner).first()
            text_analysis = ''

            text_analysis += f' {resume.training_1}'
            text_analysis += f' {resume.training_2}'
            text_analysis += f' {resume.training_3}'
            text_analysis += f' {resume.achievement_1}'
            text_analysis += f' {resume.achievement_2}'
            text_analysis += f' {resume.achievement_3}'
            text_analysis += f' {resume.experience_1}'
            text_analysis += f' {resume.experience_2}'
            text_analysis += f' {resume.experience_3}'
            text_analysis += f' {resume.summary}'
            
            job_desc = job.description.split()
            resume_text = text_analysis.split()

            common_words = set(job_desc) & set(resume_text)
            matching_word_count = len(common_words)

            if matching_word_count > 10:
                applicant = db.query(User).filter(User.id == resume.resume_owner).first()
                print(applicant.__dict__)
                
                top_applicants.append({'applicant': applicant, 'applicant_resume': resume, 'matches': matching_word_count })


        sorted_top_applicants = sorted(top_applicants, key=lambda x: x['matches'], reverse=True)
        print(sorted_top_applicants)
        return { 'response': 'applications retrieved', 'job': job, 'all_applications': all_applications, 'analysis': sorted_top_applicants, 'status_code': 200 }
    # except:
    #     return { 'response': 'applications Retrieval Failed', 'status_code': 200 }