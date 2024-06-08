from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from datetime import datetime

from models import User, Resume, Certification, Experience, JobPosting, JobApplication
from model_classes import CertModel, ResumeModel, IdModel, ExpModel
from database import get_database

import os
import tempfile


router = APIRouter()

FILESDIR = "files/"


@router.post('/submit_resume')
async def submit_resume(resume: ResumeModel, db: Session = Depends(get_database)):
    # try:
        print('Submission received')
        existing_resume = db.query(Resume).filter(Resume.resume_owner == resume.resume_owner).first()

        if not existing_resume:
            new_resume = Resume()
            new_resume.resume_owner = resume.resume_owner
            new_resume.ed_1 = resume.ed_1
            new_resume.ed_2 = resume.ed_2
            new_resume.ed_3 = resume.ed_3
            new_resume.summary = resume.summary
            new_resume.ref_1 = resume.ref_1
            new_resume.ref_2 = resume.ref_2
            new_resume.ref_3 = resume.ref_3
            db.add(new_resume)
            db.commit()

        else:
            existing_resume.resume_owner = resume.resume_owner
            existing_resume.ed_1 = resume.ed_1
            existing_resume.ed_2 = resume.ed_2
            existing_resume.ed_3 = resume.ed_3
            existing_resume.summary = resume.summary
            existing_resume.ref_1 = resume.ref_1
            existing_resume.ref_2 = resume.ref_2
            existing_resume.ref_3 = resume.ref_3
            db.commit()

        return { 'response': 'resume submitted', 'status_code': 200 }
    # except:
    #     return { 'response': 'Error retrieving data.', 'status_code': 400 }



    # for exp in resume.experiences:
    #     existing_experience = db.query(Experience).filter(Experience.resume_id == resume.resume_owner, Experience.job_title == exp.job_title, Experience.company == exp.company).first()

    #     if not existing_experience:
    #         new_experience = Experience()
    #         new_experience.job_title=exp.job_title
    #         new_experience.company=exp.company
    #         new_experience.tenure_start = datetime.strptime(exp.tenure_start, '%Y-%m-%d')
    #         new_experience.tenure_end = datetime.strptime(exp.tenure_end, '%Y-%m-%d')
    #         new_experience.resume_id=resume.resume_owner
    #         db.add(new_experience)

    #     db.commit()
            
            
@router.post('/add_certification')
async def add_certification(cert_info: CertModel, db: Session = Depends(get_database)):
    try:
        existing_certification = db.query(Certification).filter(
            Certification.title == cert_info.title, 
            Certification.training_center == cert_info.training_center).first()

        if not existing_certification:
            new_certification = Certification()
            new_certification.title=cert_info.title
            # new_certification.date=cert_info.date
            # new_certification.attachment= f"{FILESDIR}{cert_info.attachment}"
            new_certification.training_center= cert_info.training_center
            new_certification.resume_id=cert_info.id
            db.add(new_certification)

        db.commit()
        
        return { 'response': 'Certification Successfully Added', 'status_code': '200' }
    except:
        return { 'response': 'Failed to Remove Certification', 'status_code': '400' }
    

@router.post('/add_experience')
async def add_experience(exp_info: ExpModel, db: Session = Depends(get_database)):
    try:
    
        existing_experience = db.query(Experience).filter(
            Experience.job_title == exp_info.job_title, 
            Experience.company == exp_info.company,
            Experience.tenure_start == datetime.strptime(exp_info.tenure_start, '%Y-%m-%d'), 
            Experience.tenure_end == datetime.strptime(exp_info.tenure_end, '%Y-%m-%d')).first()

        if not existing_experience:
            new_experience = Experience()
            new_experience.job_title=exp_info.job_title
            new_experience.company=exp_info.company
            new_experience.tenure_start= datetime.strptime(exp_info.tenure_start, '%Y-%m-%d')
            new_experience.tenure_end= datetime.strptime(exp_info.tenure_end, '%Y-%m-%d')
            new_experience.resume_id=exp_info.id
            db.add(new_experience)

        db.commit()
        
        return { 'response': 'Experience Successfully Added', 'status_code': '200' }
    except:
        return { 'response': 'Failed to add experience', 'status_code': '400' }
    
    
@router.delete('/remove_certification')
async def remove_certification(cert_id: IdModel, db: Session = Depends(get_database)):
    try:
        cert = db.query(Certification).filter(Certification.id == cert_id.id).first()
        
        db.delete(cert)
        db.commit()
        
        return { 'response': 'Certification Successfully Removed', 'status_code': '200' }
    except:
        return { 'response': 'Failed to Remove Certification', 'status_code': '400' }


@router.delete('/remove_experience')
async def remove_experience(experience_id: IdModel, db: Session = Depends(get_database)):
    try:
        exp = db.query(Experience).filter(Experience.id == experience_id.id).first()
        
        db.delete(exp)
        db.commit()
        
        return { 'response': 'Work Experience Successfully Removed', 'status_code': '200' }
    except:
        return { 'response': 'Failed to Remove Work Experience', 'status_code': '400' }



@router.get('/show_resumes')
async def show_resumes(db: Session = Depends(get_database)):
    try:
        all_resumes = db.query(Resume).all()
        return { 'response': 'resumes retrieved', 'resumes': all_resumes, 'status_code': 200 }
    except:
        return { 'response': 'resumes Retrieval Failed', 'status_code': 200 }
    

@router.get('/retrieve_resume_data')
async def retrieve_resume_data(user_id: int, db: Session = Depends(get_database)):
    try:
        resume = db.query(Resume).filter(Resume.resume_owner == user_id).first()
        experiences = db.query(Experience).filter(Experience.resume_id == resume.id).all()
        certifications = db.query(Certification).filter(Certification.resume_id == resume.id).all()

        return { 
            'response': 'resume retrieved', 
            'resume': resume, 
            'experiences': experiences, 
            'certifications': certifications, 
            'status_code': 200
        }
    except:
        return { 'response': 'resume Retrieval Failed', 'status_code': 200 }
    
    
@router.get('/retrieve_experience_data')
async def retrieve_experience_data(user_id: int, db: Session = Depends(get_database)):
    try:
        experiences = db.query(Experience).filter(Experience.resume_id == user_id).all()

        return { 
            'response': 'Experiences retrieved', 
            'experiences': experiences,
            'status_code': 200
        }
    except:
        return { 'response': 'Experiences Retrieval Failed', 'status_code': 200 }


@router.post('/apply_to_job')
async def apply_to_job(user_id: int, job_id: int, db: Session = Depends(get_database)):
    try:
        job_id = db.query(JobPosting).filter(JobPosting.id == job_id).first()
        resume = db.query(Resume).filter(Resume.resume_owner == user_id).first()

        existing_application = db.query(JobApplication).filter(JobApplication.resume == resume.id, JobApplication.job == job_id.id).first()
        
        if existing_application is not None:
            return { 'response': 'already applied to job', 'status_code': 400 }
        
        else:
            new_application = JobApplication()
            new_application.resume = resume.id
            new_application.job = job_id.id

            db.add(new_application)
            db.commit()
            
        return { 'response': 'applied to job', 'status_code': 200 }
    except:
        return { 'response': 'Error retrieving data.', 'status_code': 400 }