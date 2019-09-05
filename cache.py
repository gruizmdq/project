from persistence import Persistence
from item import Item
import threading
import json

class Cache():
    list_items = {}
    lock_items = threading.RLock()
    needs_update = False

    @staticmethod 
    def get_item(id):
        return Cache.list_items.get(id)
    @staticmethod 
    def add_item(key, item):
        Cache.list_items.update({str(key): item})
        Cache.needs_update = True

    @staticmethod 
    def update_item(id, index=-1, file_path=-1, description=-1, status=-1):
        Cache.lock_items.acquire()
        item = Cache.get_item(id)
        
        if not item is None:
            if index != -1:
                item.index = index
            if file_path != -1:
                item.file_path = -1
            if description != -1:
                item.description = description
            if status != -1:
                item.status = status
        
            Cache.needs_update = True

        Cache.lock_items.release()

    @staticmethod 
    def update_items():
        Cache.lock_items.acquire()

        items_to_insert = []
        items_to_edit = []
        items_to_delete = []

        for i in Cache.list_items.values():
            aux = {'id': i.id, 'index': i.index, 'file_path': i.file_path, 'description': i.description}
            if i.status == 1:
                items_to_insert.append(aux)
            elif i.status == 2:
                items_to_edit.append(aux)
            elif i.status == 3:
                items_to_delete.append(aux)
        
        Persistence.update_items(items_to_insert, items_to_edit, items_to_delete)
        
        Cache.list_items.clear()
        Cache.get_items_from_db()
        Cache.lock_items.release()
    
    @staticmethod 
    def get_items_from_db():
        Cache.lock_items.acquire()
        try: 
            r = Persistence.get_items()
            for i in range(len(r)):
                new_item = Item(r[i]['description'], r[i]['file_path'], r [i]['index'], r[i]['id'], 0)
                Cache.add_item(new_item.id, new_item)
        except Exception as e:
            print(str(e))
            
        Cache.needs_update = False
        Cache.lock_items.release()

    @staticmethod
    def get_items_to_show():
        ret = {}
        for (key, value) in Cache.list_items.items():
            if value.status != 3:
                ret.update({key: value})
        return sorted(ret.values(), key=lambda x: x.index, reverse=False)