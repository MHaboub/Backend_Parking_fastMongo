from fastapi import APIRouter,HTTPException
from ...model.model_lpns import lpns
from  ...Fonctions_mdb.mongo_fcts import Mongodb_Fonctions
from configuration.conf import settings
from ..Logs import logs

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
        return "rejected"
    else :
        await logs.create_log_enter(response['userID'])
        return response['userID']
    
@router.get("/Parking/lpn_sortie")
async def lpn_exit(lpn : str):
    response = await Mongodb_Fonctions.fetch_document(collection,{"lpn":lpn})
    if response == None:
        return "NOT FOUND"
    else :
        await logs.create_log_exit(response['userID'])
        return response['userID']
    

@router.delete("/Parking/delete_Lpns_User")
async def delete_lpns_user(id : str):
    response = await Mongodb_Fonctions.remove_documents(collection,{"userID":id})
    return response