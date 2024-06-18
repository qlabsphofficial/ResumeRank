from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from datetime import datetime

from models import Notification
from database import get_database


router = APIRouter()


# NOTIFICATION ENDPOINTS
@router.post('/create_notification')
async def create_notification(applicant_id: int, job_title: str, db: Session = Depends(get_database)):
    try:
        new_notification = Notification()
        new_notification.message = 'Application Reviewed'
        new_notification.job_title = job_title
        new_notification.sent_to = applicant_id

        db.add(new_notification)
        db.commit()

        return { 'response': 'notification created', 'status_code': 200 }
    except:
        return { 'response': 'Error retrieving data.', 'status_code': 400 }
    
    
@router.get('/show_notifications')
async def get_notifications(id: int, db: Session = Depends(get_database)):
    try:
        all_notifications = db.query(Notification).filter(Notification.sent_to == id).all()

        return {'response': 'retrieval complete.', 'notifications': all_notifications}
    except:
        print('Retrieval failed.')
        return {'response': 'retrieval failed.', 'notifications': all_notifications}
    

@router.post('/delete_notifications')
async def delete_notifications(notification_id: int, db: Session = Depends(get_database)):
    try:
        delete_notification = db.query(Notification).filter(Notification.id == notification_id).first()
        
        if delete_notification:
            db.delete(delete_notification)
            db.commit()

        return { 'response': 'notification deleted.'}
    except:
        return {'response': 'failed to delete notification.'}