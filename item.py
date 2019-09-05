class Item():
    id_item = 0

    def __init__(self, description, file_path, index, id=-1, status = 1):
        self.id = int(id)
        if id == -1:
            Item.id_item += 1
            self.id = Item.id_item
        elif int(id) > Item.id_item:
            Item.id_item = int(id)

        self.description = description.replace("\r","").replace("\n","")
        self.file_path = file_path 
        #Status 0 = nothing, 1 = to insert, 2 = to edit, 3 = to delete
        self.status = status
        self.index = int(index)
    def __repr__(self):
        return '{"id": '+ str(self.id)+ ', "index": '+str(self.index) + ', "description": "'+ self.description+'", "file_path": "'+self.file_path+'"}' 