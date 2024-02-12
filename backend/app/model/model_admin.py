from pydantic import ConfigDict, BaseModel, EmailStr
from typing import List
import datetime
class CreateAdmin(BaseModel):
    name :str
    job_title : str
    company :str
    email : EmailStr
    phoneNumber :str
    guest: str  = None
    date_debut : datetime.date
    date_fin : datetime.date
    lpns : List[str] = []
    password : str
    space : str
    right : str
    model_config = ConfigDict(
        json_encoders = {
            datetime.date: lambda v: v.isoformat()  # Convert datetime.date to ISO 8601 format
        },
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "job_title": "executive assistant",
                "company" : "startup",
                "email": "jdoe@example.com",
                "phoneNumber" : "123456789",
                "guest": None,
                "date_debut": "2022-12-27",
                "date_fin" : "2024-10-10",
                "lpns": ["lpn1", "lpn2"],
                "password" : "str",
                "space" : "A-2",
                "right" : "superAdmin"
            }
        },
    )

    
class Admin(BaseModel):
    id:str
    email : EmailStr
    password : str
    space : str
    right : str
    userID : str



