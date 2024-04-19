from fastapi import APIRouter,HTTPException
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
from datetime import datetime, timedelta

collectionAuth = settings.collection_Auth
collection = settings.collection_users
url=settings.url_Auth



SECRET_KEY = "09d25e094faa6ca1122c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Auth/token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None



def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



router = APIRouter(prefix=url)
@router.post("/create")
async def create_user(user: dict):
    user1=dict(user)
    user1['date_debut'] = str(user1['date_debut'])[0:10]
    user1['date_fin'] = str(user1['date_fin'])[0:10]
    lpns_of_user = user1['lpns']
    user1['lpns'] = []
    lpn_id=[]
    print(user1)
    password_admin = user1.get("admin", {}).get("passwordAdmin", "")
    print("/**********")
    print(password_admin)
    print("/**********")
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
                    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                    access_token = create_access_token(
                    data={"sub": r["name"]}, expires_delta=access_token_expires
                   )
                    userData = {
                        "data": r,
                        "from": "server",
                        "role": "admin", 
                        "uuid": r['id'],

                    }

                    return {"access_token": access_token, "userData": userData}
            return HTTPException(status_code=403, detail="Mot de passe incorrect.")
        else:
       
            # If no document is found with the provided email or password, raise an HTTPException with status code 404
            return HTTPException(status_code=404, detail="admin not found")
    except Exception as e:
        print("*******exception***** " )
        print(e)