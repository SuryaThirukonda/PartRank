#this file has pydantic files for input validation

from pydantic import BaseModel
from datetime import datetime

#optional values 
from typing import Optional

class GPUBase(BaseModel):
    name: str
    price: Optional[float] = None
    performance: int

class GPUCreate(GPUBase):
    pass

class GPURead(GPUBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    #tells pydantic it can read data from SQLalchemy objects
    class Config: 
        orm_mode = True

class UserBase(BaseModel):
    name : str
    hashed_password: str
    email: Optional[str] = None