from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base_class import Base

class NewsletterSubscriber(Base):
    __tablename__ = "newsletter_subscribers"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    subscribed_at = Column(DateTime, default=datetime.utcnow)
