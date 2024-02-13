from backend.database.databaseConnection import database

# from motor.motor_asyncio import AsyncIOMotorError
# from pymongo.errors import PyMongoError



class Mongodb_Fonctions:
    async def insert_one(collection: str, new_data: dict)->str:
        """ return str document id """
        # result = await database[collection].insert_one(new_data)
        # print(result.inserted_id)
        try:
            result = await database[collection].insert_one(new_data)
            return str(result.inserted_id)
        except Exception as e:
            # if isinstance(e, AsyncIOMotorError):
            #     # Handle Motor async specific error
            #     print(f"An AsyncIOMotorError occurred: {e}")
            # elif isinstance(e,PyMongoError) :
            #      # Handle Motor sync specific error
            #     print(f"An PyMongoError occurred: {e}")

            # else:
            #     # Handle other exceptions
            print(f"An unexpected error occurred: {e}")
            return "Error occurred while inserting data into the database"



    async def update_document(collection: str, identifier: dict, new_data: dict):
        
        try:
            result = await database[collection].update_one(identifier, {"$set": new_data})
            if result.modified_count == 0:
                return  "Document not found or no changes made"
            return "document is updated " # Doccument is successfully updated
        except Exception as e:
            # if isinstance(e, AsyncIOMotorError):
            #     # Handle Motor async specific error
            #     print(f"An AsyncIOMotorError occurred: {e}")
            # else:
            #     # Handle other exceptions
            print(f"An unexpected error occurred: {e}")
            return "Error occurred while updating data in the database"







    async def update_all(collection: str, new_data: dict):
        try:
            result = await database[collection].update_many({}, {"$set": new_data})
            if result.modified_count == 0:
                return "Document not found or no changes made"
        
            return str(result.modified_count)+" document(s) has been updated"
        except Exception as e:
            # if isinstance(e, AsyncIOMotorError):
            #     # Handle Motor async specific error
            #     print(f"An AsyncIOMotorError occurred: {e}")
            # else:
            #     # Handle other exceptions
            print(f"An unexpected error occurred: {e}")
            return "Error occurred while updating all documents in the database"








    async def fetch_document(collection: str, identifier: dict):
        try:
            document = await database[collection].find_one(identifier)
            return document
        except Exception as e:
            # if isinstance(e, AsyncIOMotorError):
            # # Handle Motor async specific error
            #     print(f"An AsyncIOMotorError occurred: {e}")
            # else:
            #     # Handle other exceptions
            print(f"An unexpected error occurred: {e}")
            return "Error occurred while fetching data from the database"

    async def fetch_many(collection: str,identifier: dict):
        try:
            documents = []
            cursor = database[collection].find(identifier)
            async for document in cursor:
                documents.append(document)
            return documents
        except Exception as e:
            # if isinstance(e, AsyncIOMotorError):
            # # Handle Motor async specific error
            #     print(f"An AsyncIOMotorError occurred: {e}")
            # else:
            #     # Handle other exceptions
            print(f"An unexpected error occurred: {e}")
            return "Error occurred while fetching data(s) from the database"





    async def fetch_all(collection: str):
        try:
            users = []
            cursor = database[collection].find({})
            async for document in cursor:
                users.append(document)
            return users
        except Exception as e:
            # if isinstance(e, AsyncIOMotorError):
            # # Handle Motor async specific error
            #     print(f"An AsyncIOMotorError occurred: {e}")
            # else:
            #     # Handle other exceptions
            print(f"An unexpected error occurred: {e}")
            return "Error occurred while fetching all data from the database"
        








    async def remove_document(collection: str, identifier: dict) -> str:
        try:
            result= await database[collection].delete_one(identifier)
            print(identifier)
            if result.deleted_count==0:
                return "the document not fund or didn't deleted"
            return "deleted successfully "
        except Exception as e:
            # if isinstance(e, AsyncIOMotorError):
            # # Handle Motor async specific error
            #     print(f"An AsyncIOMotorError occurred: {e}")
            # else:
            #     # Handle other exceptions
            print(f"An unexpected error occurred: {e}")
            return "Error occurred while removing data from the database"

    async def remove_documents(collection: str, identifier: dict) -> str:
        try:
            print("/**********      ***********/")
            print(identifier)
            result= await database[collection].delete_many(identifier)
            print("/**********      ***********/")
            print(identifier)
            if result.deleted_count==0:
                return "the document not fund or didn't deleted"
            return str(result.deleted_count)+ " deleted successfully "
        except Exception as e:
            # if isinstance(e, AsyncIOMotorError):
            # # Handle Motor async specific error
            #     print(f"An AsyncIOMotorError occurred: {e}")
            # else:
            #     # Handle other exceptions
            print(f"An unexpected error occurred of the function remove documents : {e} *******")
            return "Error occurred while removing data(s) from the database"
