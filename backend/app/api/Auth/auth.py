from fastapi import APIRouter, Body,HTTPException
from backend.app.model.model_user_inprogress import UpdateUserData
from backend.app.model.model_users import user,CreateUser
from  backend.app.Fonctions_mdb.mongo_fcts import Mongodb_Fonctions
from configuration.conf import settings
from backend.app.api.LPNS import lpns
from bson import ObjectId
from datetime import datetime
from typing import Annotated
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel


collectionAuth = settings.collection_Auth
collection = settings.collection_users
url=settings.url_Auth



SECRET_KEY = "09d25e094faa6ca1122c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Auth/token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None








router = APIRouter(prefix=url)
@router.post("/create")
async def create_user(user: dict) -> str:
    user1=dict(user)

    user1['date_debut'] = str(user1['date_debut'])[0:10]
    user1['date_fin'] = str(user1['date_fin'])[0:10]
    lpns_of_user = user1['lpns']
    user1['lpns'] = []
    lpn_id=[]

    password_admin = user1.get("admin", {}).get("passwordAdmin", "")
    # print("/**********")
    # print(password_admin)
    # print("/**********")
    user1["admin"]["passwordAdmin"]=pwd_context.hash(password_admin)
    print("/**********")
    print(user1)
    res = await Mongodb_Fonctions.insert_one(collection,user1)
    if lpns_of_user != []:
        for lpn in lpns_of_user:
            print(lpn)
            id = await lpns.create_lpn(lpn,res)
            lpn_id.append(id)
        print(lpn_id)
        rest = await Mongodb_Fonctions.update_document(collection,{"_id":ObjectId(res)},{'lpns' : lpn_id})
        
    print(type(res))
    print("adminnnnn")
    return res
    


def get_password_hash(password):
    return pwd_context.hash(password)


@router.get("/Parking/logIn")
async def log_in(email:str , password:str):
    try : 
        
        res = await Mongodb_Fonctions.fetch_many(collection,{"email":email})
        print(res)
        if res:
            for r in res : 
                print("r = ")
                print(r)
                if r["admin"]!={} and pwd_context.verify(password,r["admin"]["passwordAdmin"]) : 
                    r['id'] = str(r.pop('_id'))
                    return r
            return HTTPException(status_code=403, detail="Mot de passe incorrect.")
        else:
       
            # If no document is found with the provided email or password, raise an HTTPException with status code 404
            return HTTPException(status_code=404, detail="admin not found")
    except Exception as e:
        print("*******exception***** " )
        print(e)





"""Application mobile"""
# User sign-in endpoint - login
@router.post('/signin')
async def sign_in(data: dict = Body(...)):
    
    user = await Mongodb_Fonctions.fetch_document(collection,{'email': data['email']})
    # collection.find_one({'email': data['email']})
    if user and user['password'] == data['password']:
        # Extract the user ID from the user document
        id = str(user['appID'])
        return {'message': 'User signed in successfully', 'userId': id}
    else:
        raise HTTPException(status_code=401, detail='User not found or password incorrect')
    



@router.put('/modifyUser/{email}')
async def update_user(email: str, data: UpdateUserData):
    
    existing_user = await Mongodb_Fonctions.fetch_document(collection,{'email': email})
    # collection.find_one({'email': email})
    
    if existing_user:
        # Extract the fields to update from the data object
        update_data = {
            'name': data.name,
            'email': data.email,
            'phone_number': data.phone_number,
            'password': data.password
        }
        
        # Perform the update operation using '$set' operator
        await Mongodb_Fonctions.update_document(collection,{'email': email},update_data)
     
        
        return {'message': 'User updated successfully'}
    else:
        raise HTTPException(status_code=404, detail='User not found')


@router.get('/user/{email}')
async def find_user_by_email(email: str):
 
    
    user = await Mongodb_Fonctions.fetch_document(collection,{'email': email})
    
    if user:
        user['_id'] = str(user['_id'])
        return {"user": user}  
    else:
        raise HTTPException(status_code=404, detail='User not found')


