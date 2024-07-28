from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.message import EmailMessage

router = APIRouter()

class EmailSchema(BaseModel):
    receiver_email: EmailStr
    subject: str
    message: str

email_address = "resumerank.notification@gmail.com"
email_password = "rghy ntrx wdio vciw"

@router.post("/send_email/")
async def send_email_route(email: EmailSchema):
    msg = EmailMessage()
    msg['Subject'] = "Email subject"
    msg['From'] = email_address
    msg['To'] = "beneboizxc@gmail.com"
    msg.set_content(
       f"""\
    It works!
    """,
         
    )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
 
    return "email successfully sent"
