from pymongo import MongoClient,InsertOne, DeleteOne, UpdateOne
import json
import constants as CONSTANTS

class Persistence():
    DB_HOST = CONSTANTS.DB_HOST
    DB_PORT = CONSTANTS.DB_PORT
    DB_NAME = CONSTANTS.DB_NAME
    COLLECTION_ITEMS = CONSTANTS.COLLECTION_ITEMS
    
    db = MongoClient(DB_HOST, DB_PORT)[DB_NAME]

    @staticmethod   
    def get_items():
        result = list(Persistence.db[Persistence.COLLECTION_ITEMS].find())
        return result

        
    @staticmethod   
    def insert_items(items):
        if not items is None:
            result = Persistence.db[Persistence.COLLECTION_ITEMS].insert_many(json.loads(items))
            return result.acknowledged
        return 0


    @staticmethod
    def update_items(insert, edit, delete):
        requests = []
        for i in insert:
            requests.append(InsertOne(i))
        for i in edit: 
            requests.append(UpdateOne({'id': i['id']}, {'$set': {'description': i['description'],'index':i['index'], 'file_path': i['file_path']}}))
        for i in delete:
            requests.append(DeleteOne({'id': i['id']}))

        result = Persistence.db[Persistence.COLLECTION_ITEMS].bulk_write(requests)
        return result.acknowledged
