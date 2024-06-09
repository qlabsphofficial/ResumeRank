from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

router = APIRouter()

class EmailSchema(BaseModel):
    receiver_email: EmailStr
    subject: str
    message: str

def send_email(receiver_email: str, subject: str, message: str):
    sender_email = "karlreubenresultan@gmail.com"
    sender_password = "test"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()

@router.post("/send_email/")
async def send_email_route(email: EmailSchema):
    try:
        send_email(email.receiver_email, email.subject, email.message)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
