from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
from docx.shared import Pt, Inches

from datetime import datetime

from models import User, Resume, Certification, Experience, JobPosting, JobApplication
from model_classes import ProfilePicModel, CertModel, ResumeModel, IdModel, UpdateProfileModel
from database import get_database

from pathlib import Path

import os
import tempfile
import shutil


router = APIRouter()

UPLOAD_DIRECTORY = Path("./uploads/profile_pictures")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


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
    # Fetch user and associated resume data
    user, resume = db.query(User, Resume).join(Resume, User.id == Resume.resume_owner).filter(User.id == user_id).first()
    experiences = db.query(Experience).filter(Experience.resume_id == resume.id).all()
    certifications = db.query(Certification).filter(Certification.resume_id == resume.id).all()

    doc = Document()

    # Set document title
    title = doc.add_heading(f'{user.firstname} {user.middlename} {user.lastname}', level=1)
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    title_format = title.paragraph_format
    title_format.space_after = Pt(0)
    title_format.line_spacing = 1.0
    
    contact_info = f'{user.email} • {user.contact_no} • @{user.firstname}.{user.lastname}'
    contact_paragraph = doc.add_paragraph(contact_info)
    contact_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    contact_paragraph_format = contact_paragraph.paragraph_format
    contact_paragraph_format.space_after = Pt(6)
    contact_paragraph_format.line_spacing = 1.0

    doc.add_paragraph()  # Add a blank line for spacing

    # Add a section for summary
    summary_heading = doc.add_heading('SUMMARY', level=2)
    summary_heading.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    summary_format = summary_heading.paragraph_format
    summary_format.space_after = Pt(6)
    summary_format.line_spacing = 1.0

    summary_paragraph = doc.add_paragraph(resume.summary)
    summary_paragraph_format = summary_paragraph.paragraph_format
    summary_paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    summary_paragraph_format.space_after = Pt(6)
    summary_paragraph_format.line_spacing = 1.0

    doc.add_paragraph()  # Add a blank line for spacing

    # Add a section for work experience
    work_exp_heading = doc.add_heading('WORK EXPERIENCE', level=2)
    work_exp_heading.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    work_exp_format = work_exp_heading.paragraph_format
    work_exp_format.space_after = Pt(6)
    work_exp_format.line_spacing = 1.0

    if experiences:
        for exp in experiences:
            exp_paragraph = doc.add_paragraph()
            exp_run = exp_paragraph.add_run(f'{exp.job_title}\n')
            exp_run.bold = True
            exp_run.font.size = Pt(12)
            exp_run.font.name = 'Arial'

            exp_paragraph.add_run(f'{exp.company}\n').font.size = Pt(11)
            exp_paragraph.add_run(f'{exp.tenure_start} - {exp.tenure_end}').font.size = Pt(10)
            exp_paragraph_format = exp_paragraph.paragraph_format
            exp_paragraph_format.space_after = Pt(6)
            exp_paragraph_format.line_spacing = 1.0

            doc.add_paragraph()  # Add a blank line for spacing
    else:
        doc.add_paragraph("No work experience provided.")

    doc.add_paragraph()  # Add a blank line for spacing

    # Add a section for certifications
    cert_heading = doc.add_heading('CERTIFICATIONS', level=2)
    cert_heading.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    cert_format = cert_heading.paragraph_format
    cert_format.space_after = Pt(6)
    cert_format.line_spacing = 1.0

    if certifications:
        for cert in certifications:
            cert_paragraph = doc.add_paragraph()
            cert_run = cert_paragraph.add_run(f'{cert.title}\n')
            cert_run.bold = True
            cert_run.font.size = Pt(12)
            cert_run.font.name = 'Arial'

            cert_paragraph.add_run(f'{cert.training_center}\n').font.size = Pt(11)
            cert_paragraph.add_run(f'{cert.date}').font.size = Pt(10)
            cert_paragraph_format = cert_paragraph.paragraph_format
            cert_paragraph_format.space_after = Pt(6)
            cert_paragraph_format.line_spacing = 1.0

            doc.add_paragraph()  # Add a blank line for spacing
    else:
        doc.add_paragraph("No certification provided.")

    # Save the document to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
        doc.save(tmp_file.name)
        tmp_file_path = tmp_file.name

    # Return the generated DOCX file as a downloadable attachment
    return FileResponse(tmp_file_path, filename=f"Resume_{user.firstname}_{user.lastname}.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

@router.get('/export_resume_to_word')
async def export_resume_to_word(user_id: int, db: Session = Depends(get_database)):
    # Fetch user and associated resume data
    user, resume = db.query(User, Resume).join(Resume, User.id == Resume.resume_owner).filter(User.id == user_id).first()
    experiences = db.query(Experience).filter(Experience.resume_id == resume.id).all()
    certifications = db.query(Certification).filter(Certification.resume_id == resume.id).all()

    doc = Document()

    # Set document title
    title = doc.add_heading(f'{user.firstname} {user.middlename} {user.lastname}', level=1)
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    title_format = title.paragraph_format
    title_format.space_after = Pt(0)
    title_format.line_spacing = 1.0
    
    contact_info = f'{user.email} • {user.contact_no} • @{user.firstname}.{user.lastname}'
    contact_paragraph = doc.add_paragraph(contact_info)
    contact_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    contact_paragraph_format = contact_paragraph.paragraph_format
    contact_paragraph_format.space_after = Pt(6)
    contact_paragraph_format.line_spacing = 1.0

    doc.add_paragraph()  # Add a blank line for spacing

    # Add a section for summary
    summary_heading = doc.add_heading('SUMMARY', level=2)
    summary_heading.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    summary_format = summary_heading.paragraph_format
    summary_format.space_after = Pt(6)
    summary_format.line_spacing = 1.0

    if resume.summary != '':
        summary_paragraph = doc.add_paragraph(resume.summary)
    else:
        summary_paragraph = doc.add_paragraph("No summary has been provided.")

    summary_paragraph_format = summary_paragraph.paragraph_format
    summary_paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    summary_paragraph_format.space_after = Pt(6)
    summary_paragraph_format.line_spacing = 1.0

    doc.add_paragraph()  # Add a blank line for spacing

    # Add a section for work experience
    work_exp_heading = doc.add_heading('WORK EXPERIENCE', level=2)
    work_exp_heading.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    work_exp_format = work_exp_heading.paragraph_format
    work_exp_format.space_after = Pt(6)
    work_exp_format.line_spacing = 1.0

    if experiences:
        for exp in experiences:
            exp_paragraph = doc.add_paragraph()
            exp_run = exp_paragraph.add_run(f'{exp.job_title}\n')
            exp_run.bold = True
            exp_run.font.size = Pt(12)
            exp_run.font.name = 'Arial'

            exp_paragraph.add_run(f'{exp.company}\n').font.size = Pt(11)
            exp_paragraph.add_run(f'{exp.tenure_start} - {exp.tenure_end}').font.size = Pt(10)
            exp_paragraph_format = exp_paragraph.paragraph_format
            exp_paragraph_format.space_after = Pt(6)
            exp_paragraph_format.line_spacing = 1.0

            doc.add_paragraph()  # Add a blank line for spacing
    else:
        doc.add_paragraph("No work experience provided.")

    doc.add_paragraph()  # Add a blank line for spacing

    # Add a section for certifications
    cert_heading = doc.add_heading('CERTIFICATIONS', level=2)
    cert_heading.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    cert_format = cert_heading.paragraph_format
    cert_format.space_after = Pt(6)
    cert_format.line_spacing = 1.0

    if certifications:
        for cert in certifications:
            cert_paragraph = doc.add_paragraph()
            cert_run = cert_paragraph.add_run(f'{cert.title}\n')
            cert_run.bold = True
            cert_run.font.size = Pt(12)
            cert_run.font.name = 'Arial'

            cert_paragraph.add_run(f'{cert.training_center}\n').font.size = Pt(11)
            cert_paragraph.add_run(f'{cert.date}').font.size = Pt(10)
            cert_paragraph_format = cert_paragraph.paragraph_format
            cert_paragraph_format.space_after = Pt(6)
            cert_paragraph_format.line_spacing = 1.0

            doc.add_paragraph()  # Add a blank line for spacing
    else:
        doc.add_paragraph("No certification provided.")

    # Save the document to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
        doc.save(tmp_file.name)
        tmp_file_path = tmp_file.name

    # Return the generated DOCX file as a downloadable attachment
    return FileResponse(tmp_file_path, filename=f"Resume_{user.firstname}_{user.lastname}.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')


# UPLOADING PROFILE PICTURE
@router.post('/upload_profile_picture')
async def upload_profile_picture(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_database)):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

    # Check if the file extension is allowed
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return { 'response': 'Invalid File Type', 'status_code': 400 }

    # Define a unique filename and save path
    unique_filename = f"user_{user_id}_profile.{file_extension}"
    file_path = UPLOAD_DIRECTORY / unique_filename

    # Save the file
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        return { 'response': 'Failed to save profile picture', 'status_code': 400 }

    # Update the user's profile picture path in the database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return { 'response': 'Failed to update profile info', 'status_code': 400 }

    user.profile_picture = str(file_path)
    db.commit()

    return {"detail": "Profile picture uploaded successfully", "file_path": str(file_path)}


@router.get('/get_profile_picture/{user_id}')
async def get_profile_picture(user_id: int, db: Session = Depends(get_database)):
    # Retrieve the user from the database
    user = db.query(User).filter(User.id == user_id).first()

    # Check if the user exists and has a profile picture
    if not user or not user.profile_picture:
        raise HTTPException(status_code=404, detail="User or profile picture not found")

    # Get the file path of the profile picture
    file_path = UPLOAD_DIRECTORY / Path(user.profile_picture).name

    # Check if the file exists
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Profile picture file not found")

    # Open the file and return its content
    with file_path.open("rb") as file:
        content = file.read()

    # Determine the content type based on the file extension
    content_type = "image/jpeg" if file_path.suffix.lower() == ".jpg" else "image/png"
    
    # Return the file content as a response with appropriate content type
    return Response(content, media_type=content_type)