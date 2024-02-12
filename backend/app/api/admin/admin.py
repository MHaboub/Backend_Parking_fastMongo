from fastapi import APIRouter,HTTPException
from ...model.model_admin import CreateAdmin,Admin
from ...model.model_users import CreateUser
from  ...Fonctions_mdb.mongo_fcts import Mongodb_Fonctions
from configuration.conf import settings
from ..users import user
from bson import ObjectId

collection = settings.collection_admins
url=settings.url_admins

router = APIRouter(prefix=url)
@router.post("/Parking/create")
async def create_admin(admin: CreateAdmin):
    user2= {
        "name" : admin.name,
        "job_title" : admin.job_title,
        "company" : admin.company,
        "email" : admin.email,
        "phoneNumber" :admin.phoneNumber,
        "guest": "native",
        "date_debut" : admin.date_debut,
        "date_fin" : admin.date_fin,
        "lpns" : admin.lpns
    }
    # user1=CreateUser.model_validate(user2)
    # print(user1)
    # print (type(user1))
    res = await user.create_user(user2)
    admin1={
        "userID": res,
        "email":admin.email,
        "password" : admin.password,
        "space" : admin.space,
        "right" : admin.right
    }
    print("userid hatha : "+ res)
    print(admin1)
    response = await Mongodb_Fonctions.insert_one(collection,admin1)
    print("w lina")
    return response





@router.get("/Parking/logIn")
async def log_in(email:str , password:str):
    try : 

        res = await Mongodb_Fonctions.fetch_document(collection,{"email":email,"password":password})

        if res:
           
            res['id'] = str(res.pop('_id'))
            return res
        else:
            # If no document is found with the provided email or password, raise an HTTPException with status code 404
            raise HTTPException(status_code=404, detail="admin not found")
    except Exception as e:
        print("*******exception***** " + e)








@router.get("/Parking/")
async def get_admins():
    responses =await Mongodb_Fonctions.fetch_all(collection)
    for response in responses:
        response_id = response.get('_id')
        if response_id:
            response['id'] = str(response.pop('_id'))

    return responses


@router.get("/Parking/{id}",response_model=Admin)
async def get_admin(id:str):
    object_id = ObjectId(id)
    response = await Mongodb_Fonctions.fetch_document(collection,{"_id":object_id})
    if response:
        response['id'] = str(response.pop('_id'))
   
        return response
    else:
        # If no document is found with the provided id, raise an HTTPException with status code 404
        raise HTTPException(status_code=404, detail="admin not found")
    








@router.put("/Parking/{id}")
async def update_admin(id:str,data:dict):
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
    result = await get_admin(id)
    userID = result['userID']
    response = await user.delete_document(userID)
    res= await Mongodb_Fonctions.remove_document(collection,{"_id":object_id})
    return res + response
