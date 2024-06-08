from fastapi import Form, UploadFile
from pydantic import BaseModel
from typing import Optional, List

class UserModel(BaseModel):
    username: str
    password: str
    firstname : str
    middlename :str
    lastname :str
    email: str
    contact_no : str
    address : str

    class Config:
        orm_mode = True


class ProfileModel(BaseModel):
    username: str = Form(...)
    firstname : str = Form(...)
    lastname : str = Form(...)
    profile_picture: Optional[UploadFile] = Form(None)
    
    
class UpdateProfileModel(BaseModel):
    id: int
    email: str
    firstname : str
    middlename: str
    lastname : str
    password: str


class JobPostingModel(BaseModel):
    title: str
    job_title: str
    description: str
    post_status: bool
    date_expired : str


class ExperienceModel(BaseModel):
    job_title: str
    company: str
    tenure_start: str
    tenure_end: str

    class Config:
        orm_mode = True
        

class ExpModel(BaseModel):
    job_title: str
    company: str
    tenure_start: str
    tenure_end: str


class CertificationModel(BaseModel):
    title: str
    training_center : str
    date: str
    attachment : Optional[UploadFile] = Form(None)

    class Config:
        orm_mode = True
        

class CertModel(BaseModel):
    title: str
    training_center : str
    date: str
    attachment : Optional[UploadFile] = Form(None)
    

class ResumeModel(BaseModel):
    resume_owner: int
    ed_1: str
    ed_2: str
    ed_3: str
    summary: str
    ref_1: str
    ref_2: str
    ref_3: str

    class Config:
        orm_mode = True


class JobPostingID(BaseModel):
    id: int


class NotificationModel(BaseModel):
    message : str
    sent_to : int


#MISC MODELS
class IdModel(BaseModel):
    id: int