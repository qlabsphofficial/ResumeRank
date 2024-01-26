from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from pydantic import BaseModel
<<<<<<< Updated upstream
from models import User, Education, Training, Experience
=======
from models import User, JobPosting, Resume, JobApplication, Notification
>>>>>>> Stashed changes
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
    user_type : bool


<<<<<<< Updated upstream
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

=======
class JobPostingID(BaseModel):
    id: int


class NotificationModel(BaseModel):
    message : str
    sent_to : int


@app.get('/show_users')
async def show_users(db: Session = Depends(get_database)):
    try:
        all_users = db.query(User).all()
        return { 'response': 'User Retrieval Success', 'users': all_users, 'status_code': 200 }
    except:
        return { 'response': 'User Retrieval Failed', 'status_code': 200 }
    
>>>>>>> Stashed changes

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
            new_user.user_type = user.user_type
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


<<<<<<< Updated upstream
@app.post('/create_training')
async def create_training(training: TrainingModel, db: Session = Depends(get_database)):
    try:
        date = datetime.strptime(training.date, "%Y-%m-%d")
=======
@app.get('/show_resumes')
async def show_resumes(db: Session = Depends(get_database)):
    # try:
        all_resumes = db.query(Resume).all()
        return { 'response': 'resumes retrieved', 'resumes': all_resumes, 'status_code': 200 }
    # except:
    #     return { 'response': 'resumes Retrieval Failed', 'status_code': 200 }
    
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream

@app.post('/create_experience')
async def create_experience(experience: ExperienceModel, db: Session = Depends(get_database)):
=======
@app.post('/delete_job_posting')
async def delete_job_posting(job: JobPostingID, db: Session = Depends(get_database)):
    try:
        retrieved_job_posting = db.query(JobPosting).filter(JobPosting.id == job.id).first()
        
        if retrieved_job_posting:
            db.delete(retrieved_job_posting)
            db.commit()

        return {'response': 'job posting deleted.'}
    except:
        return {'response': 'failed to job posting.'}


@app.get('/show_jobs')
async def show_jobs(db: Session = Depends(get_database)):
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
        return { 'response': 'Failed to save record', 'status_code': 403 }
=======
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


@app.post('/create_notification')
async def create_notification(notification: NotificationModel, db: Session = Depends(get_database)):
    try:
        new_notification = Notification()
        new_notification.message = notification.message
        new_notification.sent_to = notification.sent_to

        db.add(new_notification)
        db.commit()

        return { 'response': 'notification created', 'status_code': 200 }
    except:
        return { 'response': 'Error retrieving data.', 'status_code': 400 }
>>>>>>> Stashed changes
