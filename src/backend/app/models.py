from sqlalchemy import (Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text)
from sqlalchemy.orm import relationship
from database import Base
from datetime  import datetime

class GPU(Base):
    __tablename__ = "gpu"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float, nullable = True)
    performance = Column(Integer)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime)
