from fastapi import APIRouter,HTTPException
from ...model.model_users import user,CreateUser
from  ...Fonctions_mdb.mongo_fcts import Mongodb_Fonctions
from configuration.conf import settings
from bson import ObjectId

collection = settings.collection_users
url=settings.url_users

router = APIRouter(prefix=url)
@router.post("/Parking/create")
async def create_user(user: CreateUser):

    user1=dict(user)
    res = await Mongodb_Fonctions.insert_one(collection,user1)
    print(res)
    
    # if created_user:
    #     # If the insert operation is successful, return the created user
    #     print('sa7a')
    #     return user
    # else:
    #     # If the insert operation fails, raise an exception or handle accordingly
    #     raise HTTPException(500, "Failed to create Todo item")




@router.get("/Parking/")
async def get_users():
    responses =await Mongodb_Fonctions.fetch_all(collection)
    for response in responses:
        response_id = response.get('_id')
        if response_id:
            response['id'] = str(response.pop('_id'))

    return responses


@router.get("/Parking/{id}",response_model=user)
async def get_user(id:str):
    object_id = ObjectId(id)
    response = await Mongodb_Fonctions.fetch_document(collection,{"_id":object_id})
    if response:
       
       
        response['id'] = str(response.pop('_id'))
   
        return response
    else:
        # If no document is found with the provided id, raise an HTTPException with status code 404
        raise HTTPException(status_code=404, detail="User not found")
    
     
    




@router.put("/Parking/{id}")
async def update_user(id:str,data:dict):
    object_id = ObjectId(id)
    response = await Mongodb_Fonctions.update_document(collection,{"_id":object_id},data)
    return response





@router.put("/Parking/")
async def update_all(data:dict):
    print(data)
    response = await Mongodb_Fonctions.update_all(collection,data)
    return response


@router.delete("/Parking/{id}")
async def delete_document(id:str):
    object_id = ObjectId(id)
    res= await Mongodb_Fonctions.remove_document(collection,{"_id":object_id})
    return res
