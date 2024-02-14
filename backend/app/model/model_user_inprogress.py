from pydantic import ConfigDict, BaseModel, EmailStr
from typing import List
import datetime
class CreateuserInProggress(BaseModel):
    name :str
    job_title : str
    company :str
    email : EmailStr
    phoneNumber :str
    guest: str  = ""
    date_debut : datetime.date
    date_fin : datetime.date
    lpns : List[str] = []
    password : str
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
                "guest": "",
                "date_debut": "2022-12-27",
                "date_fin" : "2024-10-10",
                "lpns": ["lpn1", "lpn2"],
                "password" : "str",
    
            }
        },
    )



