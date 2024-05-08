import random
from fastapi import APIRouter, Body,HTTPException
from backend.app.model.model_user_inprogress import CreateuserInProggress,UpdateUserData
from  backend.app.Fonctions_mdb.mongo_fcts import Mongodb_Fonctions
from configuration.conf import settings
from backend.app.api.users import user
from bson import ObjectId
from datetime import datetime

collection = settings.collection_usersInprocess
url=settings.url_usersInprocess


# Generate random ID
def generate_unique_id():
    random_number = random.randint(100, 299)
    return random_number



router = APIRouter(prefix=url)
@router.post("/Parking/create")
async def create_user(user: dict):
    user1=dict(user)
    user1['date_debut'] = str(user1['date_debut'])
    user1['date_fin'] = str(user1['date_fin'])
    user1['Time']= datetime.now()
    user1['appID']=generate_unique_id()
    print(user1)
    res = await Mongodb_Fonctions.insert_one(collection,user1)
    print(type(res))
    return res
    

@router.get("/Parking/Processing")
async def get_users_in_progress():
    responses =await Mongodb_Fonctions.fetch_all(collection)
    for response in responses:
        response_id = response.get('_id')
        if response_id:
            response['id'] = str(response.pop('_id'))
            response['date_debut'] = datetime.strptime(response['date_debut'], '%Y-%m-%d').date()
            response['date_fin'] = datetime.strptime(response['date_fin'],'%Y-%m-%d').date()
            response['actionTime'] = datetime.now()
            print(type( response['date_fin']))

    return responses


@router.get("/Parking/Processing/{id}")
async def get_user_in_progress(id:str):
    object_id = ObjectId(id)
    response = await Mongodb_Fonctions.fetch_document(collection,{"_id":object_id})
    if response:
        response['id'] = str(response.pop('_id'))
        response['date_debut'] = datetime.strptime(response['date_debut'],'%Y-%m-%d').date()
        response['date_fin'] = datetime.strptime(response['date_fin'],'%Y-%m-%d').date()
        print(response)
        return response
    else:
        # If no document is found with the provided id, raise an HTTPException with status code 404
        return HTTPException(status_code=404, detail="User not found")
    
     
    



@router.get("/Parking/Approved_Processing/{id}")
async def approve_user_in_progress(id:str)->str:
    object_id = ObjectId(id)
    response = await get_user_in_progress(id)
    if response:
        response['admin']={}
        print(response)
        response = await user.create_user(response)
        res = await Mongodb_Fonctions.remove_document(collection,{"_id":object_id})
        print(response)
        print(res)
        return "user approved successfully"
    else:
        # If no document is found with the provided id, raise an HTTPException with status code 404
        return HTTPException(status_code=404, detail="User not found")
    
     







@router.get("/Parking/Approved_all")
async def approve_all_users()->str:
    responses = await get_users_in_progress()
    print(responses)
    for response in responses:
        response['admin']={}
        response = await user.create_user(response)
    res = await delete_all_users_in_progress()     
    print(res)
    return "all users approved successfully"
    





# @router.put("/Parking/{id}")
# async def update_user(id:str,data:dict):
#     object_id = ObjectId(id)
#     response = await Mongodb_Fonctions.update_document(collection,{"_id":object_id},data)
#     return response





# @router.put("/Parking/")
# async def update_all(data:dict):
#     print(data)
#     response = await Mongodb_Fonctions.update_all(collection,data)
#     return response


@router.delete("/Parking/delete_user_in_progress{id}")
async def delete_user_in_progress(id:str):
    object_id = ObjectId(id)
    res= await Mongodb_Fonctions.remove_document(collection,{"_id":object_id})
    return res 


@router.delete("/Parking/delete_all_progress_users/")
async def delete_all_users_in_progress():
    
    res= await Mongodb_Fonctions.remove_documents(collection,{})
    return res 





