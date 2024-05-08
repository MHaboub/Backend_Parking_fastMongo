from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from backend.database.databaseConnection import database

from backend.app.api.users import user
from backend.app.api.reports import report
from backend.app.api.LPNS import lpns
from backend.app.api.InProcess import processed
from backend.app.api.Adjustment_Records import records
from backend.app.api.Auth import auth

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



@app.on_event("startup")
async def on_startup():
    # Get the list of collections in the database
    collections = await database.list_collection_names()
    
    # Check if the database is clear (no collections or all collections are empty)
    is_db_clear = True
    
    for collection_name in collections:
        # Check the count of documents in each collection
        collection = database[collection_name]
        document_count = await collection.count_documents({})
        print("ffffff")
        print(document_count)
        if document_count > 0:
            is_db_clear = False
            break
    
    # If the database is clear, create a new user
    if is_db_clear:
        # Define the new user
        new_user = {
                "company": "startup",
                "date_debut": "2022-12-27",
                "date_fin": "2024-10-10",
                "email": "admin@admin.com",
                "job_title": "admin",
                "guest":"No",
                "lpns": [],
                "name": "Admin",
                "password": "admin",
                "gender":"Male",
                "phoneNumber": "123456789",
                "admin": {
                    "passwordAdmin": "admin",
                    "right": "SuperAdmin",
                    "space": "A-2"
                }
                }
        
            # Insert the new user into the "users" collection
        result = await auth.create_user(new_user)
            
        print(f"User created successfully with ID: {result}")
    else:
        print("Database is not clear; user creation skipped.")



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
