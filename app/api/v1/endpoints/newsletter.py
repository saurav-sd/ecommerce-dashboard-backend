from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.newsletter import NewsletterSubscriber
from app.db.schemas.newsletter import NewsletterSubscribe

router = APIRouter(
    prefix="/newsletter",
    tags=["Newsletter"],
)

@router.post("/subscribe")
def subscribe(subscriber: NewsletterSubscribe, db: Session = Depends(get_db)):
    existing = db.query(NewsletterSubscriber).filter_by(email=subscriber.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already subscribed")

    new_subscriber = NewsletterSubscriber(email=subscriber.email)
    db.add(new_subscriber)
    db.commit()
    db.refresh(new_subscriber)
    return {"message": "Subscribed successfully"}