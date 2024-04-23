from datetime import datetime,date,timedelta
import calendar
from fastapi import APIRouter
from  backend.app.Fonctions_mdb.mongo_fcts import Mongodb_Fonctions
from configuration.conf import settings
from backend.app.api.users import user
from fastapi import HTTPException

# Get the current month and year
current_month_number = datetime.now().month
current_month_name = calendar.month_name[current_month_number]
current_year = datetime.now().year

# Create the desired string
collection = f"{current_month_name}_{current_year}"
collection_log = settings.collection_logs

url=settings.url_reports

def format_date(month: str, day: str) -> str:
    """
    Convert the given month and day inputs to a date string in the format 'YYYY-MM-DD'.

    Args:
        month: The month input string in the format 'Month_Year' (e.g., 'March_2024').
        day: The day input string (e.g., '05').

    Returns:
        A date string in the format 'YYYY-MM-DD' based on the input month and day.
    """
    # Split the month input into month and year components
    month_name, year = month.split('_')
    
    # Convert month name to month number
    month_number = datetime.strptime(month_name, '%B').month
    
    # Convert inputs to integers
    year = int(year)
    day = int(day)
    
    # Create a date object
    date_obj = date(year, month_number, day)
    
    # Format the date object as a string in 'YYYY-MM-DD' format
    formatted_date = date_obj.strftime('%Y-%m-%d')
    
    return formatted_date


router = APIRouter(prefix=url)
@router.post("/Parking/enterlogs")
async def create_log_enter(userID:str):
    result = await user.get_user(userID)
    current_date = datetime.now().date()
    if  not(result['date_debut'] <= current_date <=result['date_fin'] ):
        raise HTTPException(status_code=401, detail="rejected user is suspended! ") 
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
    result = await user.get_user(userID)
    if result['guest'] == "yes":
        log = {
            'guest':"yes",
            'userID': userID,
            'action' : "exit",
            'actionTime': str(datetime.now())
        }
    else : 
        log = {
            "guest":"no",
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
            print(name)
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
    nbGuest = await Mongodb_Fonctions.count_documents(month,{"guest": "yes", "action" : "enter"})
    print(type(nbGuest))
    return nbGuest


@router.get("/Parking/get_nbNative_of_month")
async def get_nbNative_of_month(month : str)-> int:
    nbNative = await Mongodb_Fonctions.count_documents(month,{"guest": "no", "action" : "enter"})
    print(type(nbNative))
    return nbNative


@router.get("/Parking/get_nbNativeEnters")
async def get_nbNative_of_day(month : str,day : str)-> int:
    day_pattern=format_date(month,day)
    day1_pattern = f"^{day_pattern}"
    print(day1_pattern)
    # Count the documents matching the condition
    nbNativeEnter = await Mongodb_Fonctions.count_documents(
        month,  # Specify the collection
        {
            "action" : "enter",
            "guest": "no",
            "actionTime": {"$regex": day1_pattern}
        }
    )
   
    return nbNativeEnter

@router.get("/Parking/get_nbNative")
async def get_nbNative_of_day(month : str,day : str)-> int:
    day_pattern=format_date(month,day)
    day1_pattern = f"^{day_pattern}"
    print(day1_pattern)
    # Count the documents matching the condition
    nbNativeEnter = await Mongodb_Fonctions.count_documents(
        month,  # Specify the collection
        {
            "action" : "enter",
            "guest": "no",
            "actionTime": {"$regex": day1_pattern}
        }
    )
    nbNativeExit = await Mongodb_Fonctions.count_documents(
        month,  # Specify the collection
        {
            "action" : "exit",
            "guest": "no",
            "actionTime": {"$regex": day1_pattern}
        }
    )
    nbNative = nbNativeEnter - nbNativeExit
    return nbNative

@router.get("/Parking/get_nbGuestEnters")
async def get_nbGuest_of_day(month : str,day : str)-> int:
    day_pattern=format_date(month,day)
    day1_pattern = f"^{day_pattern}"
    nbGuestEnter = await Mongodb_Fonctions.count_documents(
        month,
        {
                "action" : "enter",
                "guest": "yes",
                "actionTime":{"$regex":day1_pattern}
        }
    )
    

    return nbGuestEnter

@router.get("/Parking/get_nbGuest")
async def get_nbGuest_of_day(month : str,day : str)-> int:
    day_pattern=format_date(month,day)
    day1_pattern = f"^{day_pattern}"
    nbGuestEnter = await Mongodb_Fonctions.count_documents(
        month,
        {
                "action" : "enter",
                "guest": "yes",
                "actionTime":{"$regex":day1_pattern}
        }
    )
    nbGuestExit = await Mongodb_Fonctions.count_documents(
        month,
        {
                "action" : "exit",
                "guest": "yes",
                "actionTime":{"$regex":day1_pattern}
        }
    )
    nbGuest = nbGuestEnter - nbGuestExit

    return nbGuest

@router.get("/Parking/get_ocuppied_Spots")
async def get_nbOcupied_Spots(month : str,day : str):
    nb_spot_total = 45
    day_pattern=format_date(month,day)
    day1_pattern = f"^{day_pattern}"
    nbEnter = await Mongodb_Fonctions.count_documents(month,{"actionTime":{"$regex":day1_pattern},"action":"enter"})
    nbExit = await Mongodb_Fonctions.count_documents(month,{"actionTime":{"$regex":day1_pattern},"action":"exit"})
    nb_occuppied = nbEnter - nbExit
    

    return nb_occuppied


@router.get("/Parking/get_available_Spots")
async def get_nbOcupied_Spots(month : str,day : str):
    nb_spot_total = 45
    day_pattern=format_date(month,day)
    day1_pattern = f"^{day_pattern}"
    nbEnter = await Mongodb_Fonctions.count_documents(month,{"actionTime":{"$regex":day1_pattern},"action":"enter"})
    nbExit = await Mongodb_Fonctions.count_documents(month,{"actionTime":{"$regex":day1_pattern},"action":"exit"})
    nb_occuppied = nbEnter - nbExit
    nb_available = nb_spot_total - nb_occuppied
    

    return nb_available



    

