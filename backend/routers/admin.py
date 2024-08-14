from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import desc

from datetime import datetime

from models import User, Resume, Certification, Experience, JobPosting, JobApplication, JobQualification
from model_classes import PicModel, ResumeModel, JobPostingModel, JobPostingID
from database import get_database

from pathlib import Path

import shutil


router = APIRouter()

JOB_UPLOAD_DIRECTORY = Path("./uploads/job_pictures")
JOB_UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


@router.get('/show_users')
async def show_users(db: Session = Depends(get_database)):
    try:
        all_users = db.query(User).all()
        return { 'response': 'User Retrieval Success', 'users': all_users, 'status_code': 200 }
    except:
        return { 'response': 'User Retrieval Failed', 'status_code': 200 }


@router.get('/delete_user')
async def delete_user(user_id: int, db: Session = Depends(get_database)):
    try:
        entry = db.query(User).filter(User.id == user_id).first()

        if entry:
            db.delete(entry)
            db.commit()

        return { 'response': 'Data Deleted', 'status_code': 200 }
    except:
        return { 'response': 'Error deleting data.', 'status_code': 400 }


# @router.post('/update_user')
# async def update_user(user: RegisterModel, db: Session = Depends(get_database)):
#     try:
#         existing_user = db.query(User).filter(User.id == user).first()

#         if not existing_user:
#             new_resume = Resume()
#             new_resume.resume_owner = resume.resume_owner
#             new_resume.ed_1 = resume.ed_1
#             new_resume.ed_2 = resume.ed_2
#             new_resume.ed_3 = resume.ed_3
#             new_resume.summary = resume.summary
#             new_resume.ref_1 = resume.ref_1
#             new_resume.ref_2 = resume.ref_2
#             new_resume.ref_3 = resume.ref_3
#             db.add(new_resume)
#             db.commit()

#         else:
#             existing_user.username = resume.resume_owner
#             existing_user.password = resume.ed_1
#             existing_user.first_name = resume.ed_2
#             existing_user.last_name = resume.ed_3
#             existing_user.contact = resume.summary
#             existing_user.email = resume.ref_1
#             db.commit()

#         return { 'response': 'resume submitted', 'status_code': 200 }
#     except:
#         return { 'response': 'Error retrieving data.', 'status_code': 400 }


@router.post('/create_job_posting')
async def create_job_posting(job: JobPostingModel, db: Session = Depends(get_database)):
    try:
        date_expired = datetime.strptime(job.date_expired, "%Y-%m-%d")
        
        new_job = JobPosting()
        new_job.job_title = job.job_title
        new_job.job_title = job.job_title
        new_job.description = job.description
        new_job.post_status = job.post_status
        new_job.date_expired = date_expired
        
        db.add(new_job)
        db.commit()
        
        for test in job.qualifications:
            new_qualification = JobQualification()
            new_qualification.description = test
            new_qualification.posting_id = new_job.id

            db.add(new_qualification)
            
        db.commit()

        return { 'response': 'job created', 'job_id': new_job.id, 'status_code': 200 }
    except:
        return { 'response': 'Error retrieving data.', 'status_code': 400 }
    

@router.delete('/delete_job_posting')
async def delete_job_posting(job: JobPostingID, db: Session = Depends(get_database)):
    try:
        job_exist = db.query(JobPosting).filter(JobPosting.id == job.id).first()
        
        if job_exist:
            entries = db.query(JobApplication).all()
            
            for entry in entries:
                db.delete(entry)
            db.commit()
            
            db.delete(job_exist)
            db.commit()
            
            return { 'response': 'job deleted', 'status_code': 200 }
    except:
        return { 'response': 'Error deleting data.', 'status_code': 400 }
    

@router.post('/set_job_inactive')
async def set_job_inactive(job: JobPostingID, db: Session = Depends(get_database)):
    try:
        job_exists = db.query(JobPosting).filter(JobPosting.id == job.id).first()
        
        if job_exists:
            job_exists.post_status = False
            db.commit()
            
            return { 'response': 'job deleted', 'status_code': 200 }
    except:
        return { 'response': 'Error deleting data.', 'status_code': 400 }
 
 
@router.post('/set_job_active')
async def set_job_active(job: JobPostingID, db: Session = Depends(get_database)):
    try:
        job_exists = db.query(JobPosting).filter(JobPosting.id == job.id).first()
        
        if job_exists:
            job_exists.post_status = True
            db.commit()
            
            return { 'response': 'job deleted', 'status_code': 200 }
    except:
        return { 'response': 'Error deleting data.', 'status_code': 400 }   


@router.post('/archive_user')
async def archive_user(user_id: JobPostingID, db: Session = Depends(get_database)):
    try:
        user_exists = db.query(User).filter(User.id == user_id.id).first()
        
        if user_exists:
            user_exists.is_active = False
            db.commit()
            
            return { 'response': 'User Archived', 'status_code': 200 }
    except:
        return { 'response': 'Error archiving data.', 'status_code': 400 }


@router.post('/restore_user')
async def restore_user(user_id: JobPostingID, db: Session = Depends(get_database)):
    try:
        user_exists = db.query(User).filter(User.id == user_id.id).first()
        
        if user_exists:
            user_exists.is_active = True
            db.commit()
            
            return { 'response': 'User Restored', 'status_code': 200 }
    except:
        return { 'response': 'Error restoring data.', 'status_code': 400 }


@router.get('/analytics')
async def analytics(db: Session = Depends(get_database)):
    try:
        active_users = db.query(User).filter(User.is_active == True).all()
        inactive_users = db.query(User).filter(User.is_active == False).all()
        
        active_jobs = db.query(JobPosting).filter(JobPosting.post_status == True).all()
        inactive_jobs = db.query(JobPosting).filter(JobPosting.post_status == False).all()
        
        total_applicants = db.query(JobApplication).count()
        
        
        return { 
            'response': 'User Retrieval Success', 
            'active_users': active_users,
            'inactive_users': inactive_users,
            'active_jobs': active_jobs,
            'inactive_jobs': inactive_jobs,
            'total_applicants': total_applicants,
            'status_code': 200 
        }
    except:
        return { 'response': 'User Retrieval Failed', 'status_code': 200 }


# UPLOADING JOB PICTURE
@router.post('/upload_job_picture')
async def upload_job_picture(job_id: int, file: UploadFile = File(...), db: Session = Depends(get_database)):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

    # Check if the file extension is allowed
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return { 'response': 'Invalid File Type', 'status_code': 400 }

    # Define a unique filename and save path
    unique_filename = f"job_{job_id}_profile.{file_extension}"
    file_path = JOB_UPLOAD_DIRECTORY / unique_filename

    # Save the file
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        return { 'response': 'Failed to save profile picture', 'status_code': 400 }


    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        return { 'response': 'Failed to update job info', 'status_code': 400 }

    job.picture = str(file_path)
    db.commit()

    return {"detail": "Job picture uploaded successfully", "file_path": str(file_path)}


@router.get('/get_job_picture/{job_id}')
async def get_job_picture(job_id: int, db: Session = Depends(get_database)):
    # Retrieve the user from the database
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()

    # Check if the user exists and has a profile picture
    if not job or not job.picture:
        raise HTTPException(status_code=404, detail="Job or Job picture not found")

    # Get the file path of the profile picture
    file_path = JOB_UPLOAD_DIRECTORY / Path(job.picture).name

    # Check if the file exists
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Job picture file not found")

    # Open the file and return its content
    with file_path.open("rb") as file:
        content = file.read()

    # Determine the content type based on the file extension
    content_type = "image/jpeg" if file_path.suffix.lower() == ".jpg" else "image/png"
    
    # Return the file content as a response with appropriate content type
    return Response(content, media_type=content_type)


@router.get('/applied_jobs')
async def applied_jobs(id: int, db: Session = Depends(get_database)):
    # try:
        job_postings = (
            db.query(JobPosting)
            .join(JobApplication, JobPosting.id == JobApplication.job)
            .join(Resume, JobApplication.resume == Resume.id)
            .join(User, Resume.resume_owner == User.id)
            .filter(User.id == id)
            .order_by(desc(JobApplication.id))  # Assuming `id` in JobApplication represents the application date implicitly
            .limit(5)
            .all()
        )

        if not job_postings:
            return { 'response': 'Job Application Retrieval Failed', 'status_code': 200 }

        return { 'response': 'applied jobs retrieved', 'jobs': job_postings, 'status_code': 200 }

    # except Exception as e:
    #     return { 'response': 'Job Application Retrieval Failed', 'status_code': 200 }

@router.get('/show_jobs')
async def show_jobs(db: Session = Depends(get_database)):
    try:
        all_jobs = db.query(JobPosting).all()
        return { 'response': 'jobs retrieved', 'jobs': all_jobs, 'status_code': 200 }
    except:
        return { 'response': 'User Retrieval Failed', 'status_code': 200 }


@router.post('/edit_posting_desc')
async def edit_posting_desc(id: int, desc: str, db: Session = Depends(get_database)):
    try:
        job = db.query(JobPosting).filter(JobPosting.id == id).first()
        
        job.description = desc
        db.commit()
        
        return { 'response': 'job description modified', 'status_code': 200 }
    except:
        return { 'response': 'job description modification failed', 'status_code': 200 }


@router.get('/show_active_jobs')
async def show_active_jobs(db: Session = Depends(get_database)):
    try:
        active_jobs = db.query(JobPosting).filter(JobPosting.post_status == True).all()
        return { 'response': 'active_jobs retrieved', 'active_jobs': active_jobs, 'status_code': 200 }
    except:
        return { 'response': 'Active Job Retrieval Failed', 'status_code': 200 }
    

@router.get('/show_inactive_jobs')
async def show_inactive_jobs(db: Session = Depends(get_database)):
    try:
        inactive_jobs = db.query(JobPosting).filter(JobPosting.post_status == False).all()
        return { 'response': 'inactive_jobs retrieved', 'inactive_jobs': inactive_jobs, 'status_code': 200 }
    except:
        return { 'response': 'Inactive Job Retrieval Failed', 'status_code': 200 }


@router.get('/retrieve_job_qualifications')
async def retrieve_job_qualifications(id: int, db: Session = Depends(get_database)):
    try:
        all_qualifications = db.query(JobQualification).filter(JobQualification.posting_id == id).all()
        return { 'response': 'qualifications retrieved', 'qualifications': all_qualifications, 'status_code': 200 }
    except:
        return { 'response': 'Qualifications Retrieval Failed', 'status_code': 200 }
    
    
@router.get('/show_applications')
async def show_applications(db: Session = Depends(get_database)):
    try:
        all_applications = db.query(JobApplication).all()
        return { 'response': 'applications retrieved', 'applications': all_applications, 'status_code': 200 }
    except:
        return { 'response': 'applications Retrieval Failed', 'status_code': 200 }
    

@router.get('/analyze_resumes')
async def analyze_resumes(job_id: int, db: Session = Depends(get_database)):
    try:
        job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
        all_applications = db.query(JobApplication).join(Experience, JobApplication.resume == Experience.resume_id) \
            .filter(JobApplication.job == job_id) \
            .join(Certification, JobApplication.resume == Certification.resume_id).all()
        
        job_desc = job.description.split()
        
        applicants = []
        top_applicants = []
        
        for application in all_applications:
            resume = db.query(Resume).join(User).filter(Resume.id == application.resume).filter(User.id == Resume.resume_owner).first()
            resume_analysis = ''
            
            current_points = 0

            # CHECK EDUCATIONAL ATTAINMENTS
            if resume.ed_1 and resume.ed_2 and resume.ed_3:
                current_points += 50
            elif resume.ed_1 and resume.ed_2 or resume.ed_1 and resume.ed_3 or resume.ed_2 and resume.ed_3:
                current_points += 25
            elif resume.ed_1 or resume.ed_2 or resume.ed_3:
                current_points += 10

            resume_analysis += f'{resume.summary}'

            resume_text = resume_analysis.split()

            # CHECK IF JOB DESCRIPTION MATCHES RESUME DESCRIPTION
            common_words = set(job_desc) & set(resume_text)
            current_points += len(common_words)

            
            # RATE APPLICANT BASED ON EXPERIENCE
            experiences = db.query(Experience).filter(Experience.resume_id == resume.resume_owner).all()
            
            for experience in experiences:
                experience_analysis = ''

                experience_analysis += f'{experience.job_title}'
                # experience_analysis += f'{experience.company}'
                
                if experience.tenure_end is not None:
                    difference_in_years = (experience.tenure_end - experience.tenure_start).days // 365
                else:
                    difference_in_years = (datetime.now().date() - experience.tenure_start).days // 365

                experience_text = experience_analysis.split()
                common_words = set(job_desc) & set(experience_text)

                if len(common_words) > 0:
                    current_points += difference_in_years * 50
                else:
                    current_points += difference_in_years * 20

            
            # RATE APPLICANT BASED ON CERTIFICATIONS / ACHIEVEMENTS
            certifications = db.query(Certification).filter(Certification.resume_id == resume.resume_owner).all()

            for certification in certifications:
                certification_analysis = ''

                certification_analysis += f'{certification.title}'
                # certification_analysis += f'{certification.training_center}'

                certification_text = certification_analysis.split()
                common_words = set(job_desc) & set(certification_text)

                if len(common_words) > 0:
                    current_points += 50
                else:
                    current_points += 20
                
                if certification.attachment:
                    current_points += 10

            # CHECK IF APPLICANT IS A TOP APPLICANT
            applicant = db.query(User).filter(User.id == resume.resume_owner).first()
            
            print(f'Points for Applicant {applicant.username} is: {current_points}')
            
            if current_points >= 300:    
                top_applicants.append({
                    'applicant': applicant, 
                    'applicant_resume': resume, 
                    'applicant_points': current_points, 
                    'experiences': experiences, 
                    'certifications': certifications 
                })

            else:
                applicants.append({
                    'applicant': applicant, 
                    'applicant_resume': resume, 
                    'applicant_points': current_points, 
                    'experiences': experiences, 
                    'certifications': certifications 
                })
                

        sorted_top_applicants = sorted(top_applicants, key=lambda x: x['applicant_points'], reverse=True)
        
        if sorted_top_applicants:
            return { 'response': 'applications retrieved', 'job': job, 'applicants': applicants, 'analysis': sorted_top_applicants, 'status_code': 200 }
        
        # If there are no top applicants, check if there are any applicants at all
        elif all_applications:
            return { 'response': 'no top applicants', 'job': job, 'applicants': applicants, 'status_code': 200 }
        
        # If there are no applicants at all
        else:
            return { 'response': 'no applicants', 'job': job, 'status_code': 200 }
        
    except:
        return { 'response': 'applications Retrieval Failed', 'status_code': 200 }
