from pydantic import ConfigDict, BaseModel
import datetime



class CreateRecordsAll(BaseModel):
    adminID: str
    status:str


    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "adminID": "str",
                "status":"str"

                
            }
        },
    )


class CreateRecord(BaseModel):
    adminID: str
    userID: str
    status:str
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "adminID": "str",
                "userID": "str",
                "status":"str"

                
            }
        },
    )



class RecordsAll(BaseModel):
    adminID: str
    userID: str
    time: datetime.datetime

  


class Record(BaseModel):
    adminID: str
    userID: str
    time: datetime.datetime
    status:str
    
