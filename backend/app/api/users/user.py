from fastapi import APIRouter,HTTPException
from ...model.model_users import user,CreateUser
from  ...Fonctions_mdb.mongo_fcts import Mongodb_Fonctions
from configuration.conf import settings
from ..LPNS import lpns
from bson import ObjectId
from datetime import datetime

collection = settings.collection_users
url=settings.url_users

router = APIRouter(prefix=url)
@router.post("/Parking/create")
async def create_user(user: CreateUser):
    user1=dict(user)
    user1['date_debut'] = str(user1['date_debut'])
    user1['date_fin'] = str(user1['date_fin'])
    lpnsss = user1['lpns']
    user1['lpns'] = []
    lpn_id=[]
    print('****')
    res = await Mongodb_Fonctions.insert_one(collection,user1)
    if lpns != []:
        for lpn in lpnsss:
            id = await lpns.create_lpn(lpn,res)
            lpn_id.append(id)
            print("haidlfsaqze")
        print(lpn_id)
        rest = await update_user(res , {'lpns' : lpn_id})
    print("mootaz "+res+ "  " + rest)
    print(type(res))
    return res
    


@router.get("/Parking/")
async def get_users():
    responses =await Mongodb_Fonctions.fetch_all(collection)
    for response in responses:
        response_id = response.get('_id')
        if response_id:
            response['id'] = str(response.pop('_id'))
            response['date_debut'] = datetime.strptime(response['date_debut'], '%Y-%m-%d').date()
            response['date_fin'] = datetime.strptime(response['date_fin'],'%Y-%m-%d').date()
            print(type( response['date_fin']))

    return responses


@router.get("/Parking/{id}",response_model=user)
async def get_user(id:str):
    object_id = ObjectId(id)
    response = await Mongodb_Fonctions.fetch_document(collection,{"_id":object_id})
    if response:
        response['id'] = str(response.pop('_id'))
        response['date_debut'] = datetime.strptime(response['date_debut'],'%Y-%m-%d').date()
        response['date_fin'] = datetime.strptime(response['date_fin'],'%Y-%m-%d').date()
        print(type( response['date_fin']))
   
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
    response = await lpns.delete_lpns_user(id)
    res= await Mongodb_Fonctions.remove_document(collection,{"_id":object_id})
    return res + response
