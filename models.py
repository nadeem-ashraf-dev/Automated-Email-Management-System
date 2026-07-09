from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class EmailCategory(enum.Enum):
    HIGH_PRIORITY = "high_priority"
    CUSTOMER_SUPPORT = "customer_support"
    NEWSLETTER = "newsletter"
    SPAM = "spam"
    OTHER = "other"

class EmailRecord(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True)
    gmail_message_id = Column(String, unique=True, index=True)
    subject = Column(String)
    sender = Column(String)
    body = Column(Text)
    category = Column(Enum(EmailCategory))
    confidence = Column(Integer)  # 0-100
    processed_at = Column(DateTime, default=datetime.utcnow)
    archived = Column(Integer, default=0)   # boolean
    slack_notified = Column(Integer, default=0)
    auto_replied = Column(Integer, default=0)