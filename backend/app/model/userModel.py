from pydantic import BaseModel
from typing import List, Optional

class Person(BaseModel):
    id: str = None
    avatar: Optional[str] = None
    background: Optional[str] = None
    name: str
    emails: List[dict] = []
    phoneNumbers: List[dict] = []
    title: Optional[str] = None
    company: Optional[str] = None
    birthday: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    tags: List[str] = []
