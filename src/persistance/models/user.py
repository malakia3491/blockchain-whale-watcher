import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer

from .base import BaseModel

class User(BaseModel):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(Integer, nullable=False)