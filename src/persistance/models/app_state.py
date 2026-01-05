import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer

from .base import BaseModel

class AppState(BaseModel):
    __tablename__ = 'app_states'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    last_block = Column(Integer, nullable=False)