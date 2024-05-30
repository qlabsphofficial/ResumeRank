from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_database

from models import User, Resume
from model_classes import UserModel, ProfileModel

router = APIRouter()


@router.get('/show_users')
async def show_users(db: Session = Depends(get_database)):
    try:
        all_users = db.query(User).all()
        return { 'response': 'User Retrieval Success', 'users': all_users, 'status_code': 200 }
    except:
        return { 'response': 'User Retrieval Failed', 'status_code': 200 }
    

@router.post('/login')
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


@router.post('/register')
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
            new_user.profile_picture = ''
            db.add(new_user)
            db.commit()

            newly_added = db.query(User).filter(User.username == user.username).first()

            new_resume = Resume()
            new_resume.resume_owner = newly_added.id
            new_resume.ed_1 = ''
            new_resume.ed_2 = ''
            new_resume.ed_3 = ''
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
    

@router.get('/retrieve_user_data')
async def retrieve_dashboard_data(user_id: int, db: Session = Depends(get_database)):
    try:
        user = db.query(User).filter(User.id == user_id).first()

        payload = {}
        payload.update({ 'user_data': user })

        return { 'payload': payload, 'status_code': 200 }
        
    except:
        return { 'response': 'Error retrieving data.', 'status_code': 400 }


@router.post('/edit_profile')
async def edit_profile(profile_details: ProfileModel, db: Session = Depends(get_database)):
    try:
        # file_path = f"{IMAGEDIR}{form_data.profile_picture.filename}"

        # with open(file_path, "wb") as f:
        #     contents = await form_data.profile_picture.read()
        #     f.write(contents)

        existing_user = db.query(User).filter(User.username == profile_details.username).first()
        
        if existing_user:
            print(profile_details.username)
            print(profile_details.password)
            print(profile_details.firstname)
            print(profile_details.middlename)
            print(profile_details.lastname)
            
            existing_user.username = profile_details.username
            existing_user.password = profile_details.password
            existing_user.firstname = profile_details.firstname
            existing_user.middlename = profile_details.middlename
            existing_user.lastname = profile_details.lastname
            existing_user.profile_picture = f"test"
            db.commit()
            
        return { 'response': 'Update profile successful.', 'status_code': 200 }
    except:
        return { 'response': 'update profile failed.', 'status_code': 400 }