import uuid
from sqlalchemy import Column, String, Float, UUID
from src.persistance.models import BaseModel

class Transaction(BaseModel):
    __tablename__ = 'transactions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    tx_hash = Column(String, unique=True, nullable=False, index=True)
    
    from_address = Column(String, nullable=False)
    to_address = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    symbol = Column(String, nullable=False)