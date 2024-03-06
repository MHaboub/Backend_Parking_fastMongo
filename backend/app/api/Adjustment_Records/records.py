from fastapi import APIRouter
from  backend.app.Fonctions_mdb.mongo_fcts import Mongodb_Fonctions
from configuration.conf import settings
from backend.app.model import model_record
from backend.app.api.users import user

from datetime import datetime


collection = settings.collection_record
url=settings.url_record

router = APIRouter(prefix=url)
@router.post("/Parking/create_record_all")
async def create_record_all(r : model_record.CreateRecordsAll):
    record=dict(r)
    current_date = datetime.now()
    record['time'] = str(current_date)
    name = await user.get_user(record["adminID"])
    record['AdminName'] = name['name']
    print(record)
   
    res = await Mongodb_Fonctions.insert_one(collection,record)
    print(type(res))
    return res


@router.post("/Parking/create_record")
async def create_record(r :model_record.CreateRecord):
    record=dict(r)
    current_date = datetime.now()
    record['time'] = str(current_date)
    nameadmin = await user.get_user(record["adminID"])
    record['AdminName'] = nameadmin['name']
    name = await user.get_user(record["userID"])
    record['UserName'] = name['name']
    print(record)
    res = await Mongodb_Fonctions.insert_one(collection,record)
    print(type(res))
    return res


@router.get("/Parking/get_records_all")
async def get_records_all():
    responses =await Mongodb_Fonctions.fetch_all(collection)
    for response in responses:
        response_id = response.get('_id')
        if response_id:
            response['id'] = str(response.pop('_id'))
            response['time'] = datetime.strptime(response['time'], '%Y-%m-%d %H:%M:%S.%f')
            print(type( response['time']))

    return responses


@router.get("/Parking/get_records")
async def get_record(AdminID : str):
    responses =await Mongodb_Fonctions.fetch_many(collection,{"adminID": AdminID})
    for response in responses:
        response_id = response.get('_id')
        if response_id:
            response['id'] = str(response.pop('_id'))
            response['time'] = datetime.strptime(response['time'], '%Y-%m-%d %H:%M:%S.%f')
            print(type( response['time']))

    return responses




    