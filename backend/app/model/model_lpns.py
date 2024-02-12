from pydantic import  BaseModel


class lpns(BaseModel):
    id :str
    userID: str
    lpn:str

