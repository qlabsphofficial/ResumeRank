from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from docx import Document
from docx.shared import Inches

from datetime import datetime

from models import User, Resume, Certification, Experience, JobPosting, JobApplication
from model_classes import CertModel, ResumeModel, IdModel, UpdateProfileModel
from database import get_database

import os
import tempfile


router = APIRouter()


@router.get('/retrieve_profile_info')
async def retrieve_profile_info(id: int, db: Session = Depends(get_database)):
    try:
        user = db.query(User.firstname, User.middlename, User.lastname, User.email).filter(User.id == id).first()
        
        if user is not None:
            keys = ['firstname', 'middlename', 'lastname', 'email']
            user_dict = dict(zip(keys, user))
            
            return { 'response': 'Successfully retrieved user info', 'user': user_dict, 'status_code': 200 }
        else:
            return { 'response': 'Failed to retrieve info', 'status_code': 400 }
    except:
        return { 'response': 'Failed retrieve profile info', 'status_code': 400 }


@router.post('/change_profile_info')
async def change_profile_info(profile_info: UpdateProfileModel, db: Session = Depends(get_database)):
    try:
        user = db.query(User).filter(User.id == profile_info.id).first()
        
        if user is not None:
            if profile_info.firstname != '':
                user.firstname = profile_info.firstname
                
            if profile_info.middlename != '':
                user.middlename = profile_info.middlename
                
            if profile_info.lastname != '':
                user.lastname = profile_info.lastname
                
            if profile_info.email != '':
                user.email = profile_info.email
                
            if profile_info.password != '':
                user.password = profile_info.password
             
            db.commit()
        else:
            return { 'response': 'Failed to update profile info', 'status_code': 400 }
        
        return { 'response': 'Successfully updated profile info', 'status_code': 200 }
    except:
        return { 'response': 'Failed to update profile info', 'status_code': 400 }


@router.get('/export_resume_to_word')
async def export_resume_to_word(user_id: int, db: Session = Depends(get_database)):
    # try:
        user, resume = db.query(User, Resume).join(Resume, User.id == Resume.resume_owner).filter(User.id == user_id).first()
        experience = db.query(Experience).filter(Experience.resume_id == user_id).all()
        certification = db.query(Certification).filter(Certification.resume_id == user_id).all()

        doc = Document()
        doc.add_heading(f'{user.firstname} {user.middlename} {user.lastname}', 1)
        doc.add_paragraph(f'{user.email} • {user.contact_no} • @{user.firstname}.{user.lastname}')

        doc.add_heading(f'SUMMARY', 2)
        doc.add_paragraph(f'{resume.summary}')

        doc.add_heading(f'WORK EXPERIENCE', 3)

        for exp in experience:
            doc.add_heading(f'{exp.job_title}                                                                                                                 {exp.tenure_start} - {exp.tenure_end}', 3)
            doc.add_paragraph(f'{exp.company}')

        doc.add_heading(f'CERTIFICATION', 3)
        
        for certs in certification:
            doc.add_heading(f'{certs.title}                                                                                                                                      {certs.date}', 3)
            doc.add_paragraph(f'{certs.training_center}')

        # Save the document
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            doc.save(tmp_file.name)
            tmp_file_path = tmp_file.name

        # Return the generated DOCX file as a downloadable attachment
        return FileResponse(tmp_file_path, filename=f"Resume.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

        
    # except:
    #     return { 'response': 'resume Retrieval Failed', 'status_code': 200 }