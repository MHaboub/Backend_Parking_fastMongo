from fastapi import APIRouter
from ..model import Person
from  ..mongo_fcts import Mongodb_Fonctions
from configuration.conf import settings

collection = settings.collection_user
url=settings.url_user

router = APIRouter(prefix=url)
@router.post("/Parking/create")
async def create_user(Person: Person):

    Person1=dict(Person)
    res = await Mongodb_Fonctions.insert_one(collection,Person1)
    print(res)
    
    # if created_Person:
    #     # If the insert operation is successful, return the created Person
    #     print('sa7a')
    #     return Person
    # else:
    #     # If the insert operation fails, raise an exception or handle accordingly
    #     raise HTTPException(500, "Failed to create Todo item")




@router.get("/Parking/")
async def get_users():
    response =await Mongodb_Fonctions.fetch_all(collection)
    return response


@router.get("/Parking/{id}",response_model=Person)
async def get_user(id:str):
    response = await Mongodb_Fonctions.fetch_document(collection,{"id":id})
    return response
    




@router.put("/Parking/{id}")
async def update_user(id:str,data:dict):
    response = await Mongodb_Fonctions.update_document(collection,{"id":id},data)
    return response





@router.put("/Parking/")
async def update_all(data:dict):

    
    print(type(data))
    
    response = await Mongodb_Fonctions.update_all(collection,data)
    return response


@router.delete("/Parking/{id}")
async def delete_document(id):
    res= await Mongodb_Fonctions.remove_document(collection,{"id":id})
    return res
