from pydantic import ConfigDict, BaseModel, EmailStr
from typing import List
import datetime
class CreateUser(BaseModel):
    name :str
    job_title : str
    company :str
    email : EmailStr
    phoneNumber :str
    guest: str  = None
    date_debut : datetime.date
    date_fin : datetime.date
    lpns : List[str] = []
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
                "lpns": ["lpn1", "lpn2"]
            }
        },
    )

    
class user(BaseModel):
    id:str
    name :str
    job_title : str
    company :str
    email : EmailStr
    phoneNumber :str
    lpns : List[str] = []
    guest: str = None
    date_debut : datetime.date
    date_fin : datetime.date






























    # model_config = ConfigDict(
    #     populate_by_name=True,
    #     arbitrary_types_allowed=True,
    #     json_encoders={ObjectId: str},
    #     json_schema_extra={
    #         "example": {
                
    #             "name": "Jane Doe",
    #             "job_title": "executive assistant",
    #             "company" : "startup",
    #             "email": "jdoe@example.com",
    #             "phoneNumber" : "123456789",
    #             "lpns": ["lpn1", "lpn2"]
    #         }
    #     },
    # )


# class UpdateUser(BaseModel):
#     name: Optional[str]
#     job_title: Optional[str]
#     company: Optional[str]
#     email: Optional[EmailStr]
#     phoneNumber: Optional[str]
#     lpns: Optional[List[str]]

#     model_config = ConfigDict(
#         arbitrary_types_allowed=True,
#         json_encoders={ObjectId: str},
#         json_schema_extra={
#             "example": {
#                 "name": "Jane Doe",
#                 "job_title": "executive assistant",
#                 "company": "startup",
#                 "email": "jdoe@example.com",
#                 "phoneNumber": "123456789",
#                 "lpns": ["lpn1", "lpn2"]
#             }
#         },
#     )


