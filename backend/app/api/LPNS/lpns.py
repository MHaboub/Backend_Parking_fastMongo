from fastapi import APIRouter,HTTPException
from backend.app.model.model_lpns import lpns
from  backend.app.Fonctions_mdb.mongo_fcts import Mongodb_Fonctions
from configuration.conf import settings
from backend.app.api.reports import report
from bson import ObjectId

collection = settings.collection_lpns
url=settings.url_lpns


router = APIRouter(prefix=url)
@router.post("/Parking/createlpns")
async def create_lpn(lpn: str,userID : str):
    lpns = {
        'lpn': lpn,
        'userID' : userID
    }
    res = await Mongodb_Fonctions.insert_one(collection,lpns)
    print("haboub"+res)
    return res

@router.get("/Parking/verifier_lpn")
async def verifier_lpn_enter(lpn : str):
    response = await Mongodb_Fonctions.fetch_document(collection,{"lpn":lpn})
    if response == None:
        raise HTTPException(status_code=400, detail="Rejected !! ")
    else :
        print("lhna")
        return await report.create_log_enter(response['userID'])
    
@router.get("/Parking/lpn_sortie")
async def lpn_exit(lpn : str):
    response = await Mongodb_Fonctions.fetch_document(collection,{"lpn":lpn})
    if response == None:
        raise HTTPException(status_code=400, detail="NOT FOUND") 
    else :
        await report.create_log_exit(response['userID'])
        return response['userID']
    



@router.get("/Parking/get_lpn_user")
async def get_all_lpns_user(id : str):
    responses = await Mongodb_Fonctions.fetch_many(collection,{"userID":id})
    lpn =[]
    for response in responses:
        response_id = response.get('_id')
        if response_id:
            response['id'] = str(response.pop('_id'))
            lpn.append(response['lpn'])
    return lpn



@router.get("/Parking/get_lpn")
async def get_lpn(id : str):
    object_id = ObjectId(id)
    response = await Mongodb_Fonctions.fetch_document(collection,{"_id":object_id})
    if response:
        response['id'] = str(response.pop('_id'))
        return response
    else:
        # If no document is found with the provided id, raise an HTTPException with status code 404
        raise HTTPException(status_code=404, detail="User not found")
    


    


@router.delete("/Parking/delete_Lpns_User")
async def delete_lpns_user(id : str):
    response = await Mongodb_Fonctions.remove_documents(collection,{"userID":id})
    return response