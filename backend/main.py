from fastapi import FastAPI, Depends, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base

from routers import admin, authentication, notifications, resume, profile


IMAGEDIR = "images/"

app = FastAPI()
app.include_router(admin.router)
app.include_router(authentication.router)
app.include_router(notifications.router)
app.include_router(resume.router)
app.include_router(profile.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)