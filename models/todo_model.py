from pydantic import BaseModel, Field
from typing import Optional

class TodoCreate(BaseModel):
    id: Optional[str] = None
    description: str = Field(..., description='Detailed description of the todo')
    completed: Optional[bool] = False
    created_at: Optional[str] = None
    
class TodoUpdate(BaseModel):
    id: Optional[str] = None
    description: Optional[str] = None 
    completed: Optional[bool] = False
    created_at: Optional[str] = None