from pydantic import ConfigDict, BaseModel
import datetime

datetime=str(datetime.datetime.now())


class CreateLogs(BaseModel):
    idUser: str
    action: str
    actionTime: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "idUser": "ex",
                "action": "action",
                "actionTime": "2024-02-07 14:17:10.146372"

                
            }
        },
    )

    
class Logs(BaseModel):
    id:str 
    idUser: str
    action: str
    actionTime: str
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "idUser": "ex",
                "action": "action",
                "actionTime": "2024-02-07 14:17:10.146372"
            }
        },
    )