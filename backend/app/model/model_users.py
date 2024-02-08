from pydantic import ConfigDict, BaseModel, Field, EmailStr
# from pydantic.functional_validators import BeforeValidator
from typing import List, Optional
from bson import ObjectId
from typing_extensions import Annotated

# PyObjectId = Annotated[str, BeforeValidator(str)]

class CreateUser(BaseModel):
    name :str
    job_title : str
    company :str
    email : EmailStr
    phoneNumber :str
    lpns : List[str] = []
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                
                "name": "Jane Doe",
                "job_title": "executive assistant",
                "company" : "startup",
                "email": "jdoe@example.com",
                "phoneNumber" : "123456789",
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


