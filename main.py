from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.users import user

from backend.app.api.admin import admin

from backend.app.api.LPNS import lpns

from backend.app.api.Logs import logs

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=['*']
)


@app.get("/")
def read_Root():
    return {"haboub":"YA MAALEM!!!!!"}

app.include_router(user.router,tags=["Users"])
app.include_router(admin.router,tags=["Admins"])
app.include_router(lpns.router,tags=["LPNS"])
app.include_router(logs.router,tags=["Logs"])