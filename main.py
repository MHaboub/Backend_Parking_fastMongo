from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.app.api.users import user
from backend.app.api.reports import report
from backend.app.api.LPNS import lpns
from backend.app.api.InProcess import processed
from backend.app.api.Adjustment_Records import records
from backend.app.api.Auth import auth

# from backend.app.api.Logs import logs

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
    return {"haboub": "YA MAALEM!!!!!"}

app.include_router(user.router, tags=["Users"])
app.include_router(processed.router, tags=["Users In Process"])
app.include_router(records.router, tags=["records"])
app.include_router(auth.router, tags=["Auth"])
# app.include_router(admin.router, tags=["Admins"])
app.include_router(lpns.router, tags=["LPNS"])
# app.include_router(logs.router, tags=["Logs"])
app.include_router(report.router, tags=["reports"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
