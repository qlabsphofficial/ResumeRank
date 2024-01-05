from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from pydantic import BaseModel
from models import User
import datetime as dt


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


class LogModel(BaseModel):
    turbidity: int
    humidity: int
    tds: int
    user_id: int



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
    # try:
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
    # except:
    #     return { 'response': 'Registration failed.', 'status_code': 400 }


@app.post('/insert_entry')
async def insert_log(log: LogModel, db: Session = Depends(get_database)):
    try:
        new_entry = Log()
        new_entry.turbidity = log.turbidity
        new_entry.humidity = log.humidity 
        new_entry.tds = log.tds
        new_entry.date_created = dt.datetime.now()
        new_entry.record_owner = log.user_id

        db.add(new_entry)
        db.commit()
        
        return { 'response': 'Log added.', 'status_code': 200 }
    except:
        return { 'response': 'Failed to add log.', 'status_code': 403 }


@app.get('/all_entries')
async def retrieve_entries(user_id: int, db: Session = Depends(get_database)):
    try:
        entries = db.query(Log).filter(Log.record_owner == user_id).all()

        return { 'payload': entries, 'status_code': 200 }
    except:
        return { 'response': 'Error retrieving data.', 'status_code': 400 }