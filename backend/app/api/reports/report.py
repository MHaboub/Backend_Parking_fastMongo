from datetime import datetime
import calendar
from fastapi import APIRouter
from  backend.app.Fonctions_mdb.mongo_fcts import Mongodb_Fonctions
from configuration.conf import settings
from backend.app.api.users import user

# Get the current month and year
current_month_number = datetime.now().month
current_month_name = calendar.month_name[current_month_number]
current_year = datetime.now().year

# Create the desired string
collection = f"{current_month_name}_{current_year}"
collection_log = settings.collection_logs

url=settings.url_reports




router = APIRouter(prefix=url)
@router.post("/Parking/enterlogs")
async def create_log_enter(userID:str):
    result = await user.get_user(userID)
    current_date = datetime.now().date()
    if  not(result['date_debut'] <= current_date <=result['date_fin'] ):
        return "rejected user is suspended! "
    if result['guest'] == "yes":
        log = {
        'guest':"yes",
        'userID': userID,
        'action' : "enter",
        'actionTime': str(datetime.now())
        }
    else : 
        log = {
            "guest":"no",
            'userID': userID,
            'action' : "enter",
            'actionTime': str(datetime.now())
        }
    print(collection)
    res =await Mongodb_Fonctions.insert_one(collection,log)
    
    resu = await Mongodb_Fonctions.insert_one(collection_log,log)
    return res + resu

@router.post("/Parking/exitlogs")
async def create_log_exit(userID:str):
    log = {
        'userID': userID,
        'action' : "exit",
        'actionTime': str(datetime.now())
    }
    res =await Mongodb_Fonctions.insert_one(collection,log)
    resu = await Mongodb_Fonctions.insert_one(collection_log,log)
    
    return res + resu




@router.get("/Parking/get_all_logs")
async def get_all_logs():
    responses = await Mongodb_Fonctions.fetch_all(collection_log)
    print(responses)
    for response in responses:
        print(response)
        response_id = response.get('_id')
        if response_id:
            print("----------------")
            response['id'] = str(response.pop('_id'))
            print(response["userID"])
            name = await user.get_user(response["userID"])
            response['name']= name['name']
            print(type(response['actionTime']))
            print("/**********/")
            print(response)
    
    return responses

@router.get("/Parking/get_logs")
async def get_logs(nb : int):
    responses = await Mongodb_Fonctions.fetch_all(collection)
    print(responses)
    for response in responses:
        print(response)
        response_id = response.get('_id')
        if response_id:
            response['id'] = str(response.pop('_id'))
            print(response["userID"])
            name = await user.get_user(response["userID"])
            print(name)
            response['name']= name['name']
            print(type(response['actionTime']))
    if len(responses)>=nb:
        return responses[:-(nb+1):-1]
    
    else :
        return responses



@router.get("/Parking/get_nbGuest_of_the_month")
async def get_nbGuest_of_month(month : str)-> int:
    nbGuest = await Mongodb_Fonctions.count_documents(month,{"guest": "yes"})
    print(type(nbGuest))
    return nbGuest


@router.get("/Parking/get_nbNative_of_month")
async def get_nbNative_of_month(month : str)-> int:
    nbNative = await Mongodb_Fonctions.count_documents(month,{"guest": "no"})
    print(type(nbNative))
    return nbNative




@router.get("/Parking/get_nbNative")
async def get_nbNative_of_day(month : str,day : str)-> int:
    day1=f"^{day}"
    print(day1)
    nbNative = await Mongodb_Fonctions.count_documents(month,{"guest": "no","actionTime":{"$regex":day1}})
    print(type(nbNative))
    return nbNative




@router.get("/Parking/get_nbGuest")
async def get_nbGuest_of_day(month : str,day : str)-> int:
    day1=f"^{day}"
    print(day1)
    nbGuest = await Mongodb_Fonctions.count_documents(month,{"guest": "no","actionTime":{"$regex":day1}})
    print(type(nbGuest))
    return nbGuest

@router.get("/Parking/get_nbOcupied_Spots")
async def get_nbOcupied_Spots(month : str,day : str)-> int:
    day1=f"^{day}"
    nbEnter = await Mongodb_Fonctions.count_documents(month,{"actionTime":{"$regex":day1},"action":"enter"})
    nbExit = await Mongodb_Fonctions.count_documents(month,{"actionTime":{"$regex":day1},"action":"exit"})
    nbOccupied = nbEnter - nbExit
    return nbOccupied


