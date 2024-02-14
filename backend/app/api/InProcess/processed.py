from fastapi import APIRouter,HTTPException
from backend.app.model.model_user_inprogress import CreateuserInProggress
from  backend.app.Fonctions_mdb.mongo_fcts import Mongodb_Fonctions
from configuration.conf import settings
from backend.app.api.users import user
from bson import ObjectId
from datetime import datetime

collection = settings.collection_usersInprocess
url=settings.url_usersInprocess

router = APIRouter(prefix=url)
@router.post("/Parking/create")
async def create_user(user: CreateuserInProggress):
    user1=dict(user)
    user1['date_debut'] = str(user1['date_debut'])
    user1['date_fin'] = str(user1['date_fin'])
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
    response = await Mongodb_Fonctions.fetch_document(collection,{"_id":object_id})
    if response:
        response['id'] = str(response.pop('_id'))
        response['date_debut'] = datetime.strptime(response['date_debut'],'%Y-%m-%d').date()
        response['date_fin'] = datetime.strptime(response['date_fin'],'%Y-%m-%d').date()
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




