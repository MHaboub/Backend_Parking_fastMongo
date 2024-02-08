from pydantic import ConfigDict, BaseModel


class CreateReports(BaseModel):
    nbSpotsAvailable: int
    nbSpotsOccupied: int
    nbGests: int
    nbNative: int
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "nbSpotsAvailable": 1,
                "nbSpotsOccupied":1 ,
                "nbGests": 1,
                "nbNative": 1
                
            }
        },
    )

    
class Reports(BaseModel):
    id:str 
    nbSpotsAvailable: int
    nbSpotsOccupied: int
    nbGests: int
    nbNative: int
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "nbSpotsAvailable": 1,
                "nbSpotsOccupied":1 ,
                "nbGests": 1,
                "nbNative": 1
            }
        },
    )