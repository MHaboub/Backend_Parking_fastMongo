from fastapi import APIRouter,HTTPException
from backend.app.model.model_users import user,CreateUser
from  backend.app.Fonctions_mdb.mongo_fcts import Mongodb_Fonctions
from configuration.conf import settings
from backend.app.api.LPNS import lpns
from bson import ObjectId
from datetime import datetime

collection = settings.collection_users
url=settings.url_users

router = APIRouter(prefix=url)
@router.post("/Parking/create")
async def create_user(user: dict):
    user1=dict(user)
    user1['date_debut'] = str(user1['date_debut'])[0:10]
    user1['date_fin'] = str(user1['date_fin'])[0:10]
    lpns_of_user = user1['lpns']
    user1['lpns'] = []
    lpn_id=[]
    print(user1)
    res = await Mongodb_Fonctions.insert_one(collection,user1)
    if lpns_of_user != []:
        for lpn in lpns_of_user:
            print(lpn)
            id = await lpns.create_lpn(lpn,res)
            lpn_id.append(id)
        print(lpn_id)
        rest = await Mongodb_Fonctions.update_document(collection,{"_id":ObjectId(res)},{'lpns' : lpn_id})
        print("mootaz "+res+ "  " + rest)
    print(type(res))
    return res
    



@router.get("/Parking/logIn")
async def log_in(email:str , password:str):
    try : 

        res = await Mongodb_Fonctions.fetch_document(collection,{"email":email,"admin.passwordAdmin":password})

        if res:
           
            res['id'] = str(res.pop('_id'))
            return res
        else:
       
            # If no document is found with the provided email or password, raise an HTTPException with status code 404
            return HTTPException(status_code=404, detail="admin not found")
    except Exception as e:
        print("*******exception***** " )
        print(e)


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


@router.get("/Parking/get_admins")
async def get_admins():
    responses =await Mongodb_Fonctions.fetch_many(collection,{
  "admin": { "$exists": True, "$ne": {} },
  "admin.space": { "$ne": "" }
})
    print(responses)
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
        if response['lpns'] !=[]:
            response['lpns']=[]

            response['lpns'] = await lpns.get_all_lpns_user(id)

        print(type( response['guest']))
        print(response)
        return response
    else:
        # If no document is found with the provided id, raise an HTTPException with status code 404
        raise HTTPException(status_code=404, detail="User not found")
    
     
    




@router.put("/Parking/{id}")
async def update_user(id:str,data:dict):
    object_id = ObjectId(id)
    print("/*******")
    print(type(data['lpns']))
    data['lpns'] =await comparision_lpns(id, data['lpns'])
    data['date_debut'] = str(data['date_debut'])[0:10]
    data['date_fin'] = str(data['date_fin'])[0:10]
    response = await Mongodb_Fonctions.update_document(collection,{"_id":object_id},data)
    return response


@router.get("/Parking/comparision_lpns")
async def comparision_lpns(userid :str,lpn:list)->list:
    object_id = ObjectId(userid)
    res = await Mongodb_Fonctions.fetch_document(collection,{"_id":object_id})
    lpn1 = await lpns.get_all_lpns_user(userid)
    print("il res = ")
    print(res)
    print(lpn1)
    print("/*******")
    print(lpn)
    print("******")
    print(res['lpns'])
    if lpn1 == lpn:
        print("********/")
        print(res['lpns'])
        return res['lpns']
    else:
        await lpns.delete_lpns_user(userid)
        lpn_id=[]
        for lpn1 in lpn:
            id = await lpns.create_lpn(lpn1,userid)
            lpn_id.append(id)
        return lpn_id

 




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


