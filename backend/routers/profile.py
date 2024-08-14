from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt, RGBColor, Inches
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from tempfile import NamedTemporaryFile
from docx2pdf import convert

from datetime import datetime

from models import User, Resume, Certification, Experience, JobPosting, JobApplication
from model_classes import PicModel, CertModel, ResumeModel, IdModel, UpdateProfileModel
from database import get_database

from pathlib import Path

import os
import tempfile
import shutil
import subprocess

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


def add_styled_paragraph(cell, text, bold=False, font_size=Pt(12), font_color=RGBColor(0, 0, 0), alignment=WD_PARAGRAPH_ALIGNMENT.LEFT):
    paragraph = cell.add_paragraph()
    run = paragraph.add_run(text)
    font = run.font
    font.bold = bold
    font.name = 'Century Gothic'
    font.size = font_size
    font.color.rgb = font_color
    paragraph.alignment = alignment
    return paragraph

def add_section_heading(cell, heading_text, level=2):
    paragraph = cell.add_paragraph()
    run = paragraph.add_run(heading_text)
    run.bold = True
    run.font.size = Pt(14 if level == 2 else 12)
    run.font.color.rgb = RGBColor(54, 95, 145)  # Dark Blue
    run.font.name = 'Century Gothic'
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    paragraph.paragraph_format.space_after = Pt(6)
    paragraph.paragraph_format.line_spacing = 1.0

def set_cell_border(cell, **kwargs):
    """
    Set cell's border
    Usage:

    set_cell_border(cell, top={"sz": 12, "val": "single", "color": "#000000", "space": "0"},
                         bottom={"sz": 12, "val": "single", "color": "#000000", "space": "0"},
                         left={"sz": 12, "val": "single", "color": "#000000", "space": "0"},
                         right={"sz": 12, "val": "single", "color": "#000000", "space": "0"})
    """
    tc = cell._element.tc
    tcPr = tc.get_or_add_tcPr()
    for edge in ('top', 'left', 'bottom', 'right'):
        if edge in kwargs:
            edge_data = kwargs[edge]
            tag = 'w:{}'.format(edge)
            element = tcPr.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcPr.append(element)
            for key in ["sz", "val", "color", "space"]:
                if key in edge_data:
                    element.set(qn('w:{}'.format(key)), str(edge_data[key]))

@router.get('/export_resume_to_word')
async def export_resume_to_word(user_id: int, db: Session = Depends(get_database)):
    user, resume = db.query(User, Resume).join(Resume, User.id == Resume.resume_owner).filter(User.id == user_id).first()
    experiences = db.query(Experience).filter(Experience.resume_id == resume.id).all()
    certifications = db.query(Certification).filter(Certification.resume_id == resume.id).all()

    doc = Document()

    # Adding a two-column layout using a table
    table = doc.add_table(rows=1, cols=2)
    table.autofit = False
    column_widths = [Inches(3.2), Inches(3.3)]
    for col, width in zip(table.columns, column_widths):
        for cell in col.cells:
            cell.width = width

    # Left Column (Profile, Contact Info, Education, etc.)
    cell_left = table.cell(0, 0)
    cell_left.vertical_alignment = WD_ALIGN_VERTICAL.TOP

    # Right Column (Experience, Certifications, etc.)
    cell_right = table.cell(0, 1)
    cell_right.vertical_alignment = WD_ALIGN_VERTICAL.TOP

    # Profile Picture (Placeholder)
    # Uncomment the next line to add a real picture
    cell_left.paragraphs[0].add_run().add_picture(f'{user.profile_picture}', width=Inches(1.25))

    # Name and Title
    add_styled_paragraph(cell_right, f'{user.firstname} {user.middlename} {user.lastname}', bold=True, font_size=Pt(30), alignment=WD_PARAGRAPH_ALIGNMENT.LEFT)

    # Summary
    add_section_heading(cell_right, '', level=3)
    add_section_heading(cell_right, 'SUMMARY', level=3)
    if resume.summary:
        add_styled_paragraph(cell_right, resume.summary, font_size=Pt(10), font_color=RGBColor(0, 0, 0))
    else:
        add_styled_paragraph(cell_right, "No summary has been provided.", font_size=Pt(10), font_color=RGBColor(0, 0, 0))

    # Contact Info
    add_section_heading(cell_left, '', level=3)
    add_section_heading(cell_left, 'CONTACT', level=3)
    add_styled_paragraph(cell_left, f'Phone\n{user.contact_no}', font_size=Pt(10))
    add_styled_paragraph(cell_left, f'Email\n{user.email}', font_size=Pt(10))
    add_styled_paragraph(cell_left, f'Address\n{user.address}', font_size=Pt(10))

    # Education
    add_section_heading(cell_left, '', level=3)
    add_section_heading(cell_left, 'EDUCATION', level=3)
    if resume.ed_1:
        add_styled_paragraph(cell_left, f'Primary Education\n{resume.ed_1}', font_size=Pt(10))
    if resume.ed_2:
        add_styled_paragraph(cell_left, f'Secondary Education\n{resume.ed_2}', font_size=Pt(10))
    if resume.ed_3:
        add_styled_paragraph(cell_left, f'Tertiary Education\n{resume.ed_3}', font_size=Pt(10))

    # Work Experience
    add_section_heading(cell_right, '', level=3)
    add_section_heading(cell_right, 'EXPERIENCE', level=3)
    if experiences:
        for exp in experiences:
            exp_paragraph = add_styled_paragraph(cell_right, f'{exp.job_title}\n{exp.company}\n{exp.tenure_start} - {exp.tenure_end}', bold=False, font_size=Pt(10), font_color=RGBColor(0, 0, 0))
    else:
        add_styled_paragraph(cell_right, "No work experience provided.", font_size=Pt(10), font_color=RGBColor(77, 77, 77))

    # Certifications
    add_section_heading(cell_right, '', level=3)
    add_section_heading(cell_right, 'CERTIFICATIONS', level=3)
    if certifications:
        for cert in certifications:
            add_styled_paragraph(cell_right, f'{cert.title}\n{cert.training_center}\n{cert.date}', bold=False, font_size=Pt(10), font_color=RGBColor(0, 0, 0))
    else:
        add_styled_paragraph(cell_right, "No certification provided.", font_size=Pt(10), font_color=RGBColor(77, 77, 77))

    # Save the document to a temporary file
    with NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
        doc.save(tmp_file.name)
        tmp_file_path = tmp_file.name

    # Convert the DOCX file to PDF
    try:
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', tmp_file_path], check=True)
        print(f"Successfully converted {tmp_file_path} to PDF.")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        
    # pdf_path = tmp_file_path.replace('.docx', '.pdf')
    # convert(tmp_file_path, pdf_path)

    # Remove the temporary DOCX file
    os.remove(tmp_file_path)

    # Return the generated PDF file as a downloadable attachment
    return FileResponse(tmp_file_path, filename=f"Resume_{user.firstname}_{user.lastname}.pdf", media_type='application/pdf')


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