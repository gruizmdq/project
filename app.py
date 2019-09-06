from flask import Flask, Response, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, send, emit
from PIL import Image
import os
import threading
from cache import Cache
from item import Item
import time as Time
import json
import constants as CONSTANTS


app = Flask(__name__)
socketio = SocketIO(app)

#INDEX
@app.route("/")
def index():
    return render_template('index.html', items = Cache.get_items_to_show())

@app.route("/delete_image", methods=['POST'])
def delete_image():
    if not request.form['id'] is None:
        if not Cache.get_item(request.form['id']) is None:
            Cache.update_item(id=request.form['id'], status = 3)
            try:
                os.remove(Cache.get_item(request.form['id']).file_path)
            except Exception as e:
                print(e)
    
    socketio.emit('delete_item', request.form['id'] ,namespace='/app')
    return Response('200', status='200')

@app.route("/edit_indexes", methods=['POST'])
def edit_indexes():
    data = request.get_json()
    for i in data:
        Cache.update_item(id = i['id'], index = i['index'], status = 2)
    
    #unorthodox way to create a json
    j = '{"data": ['
    for i in sorted(Cache.list_items.values(), key=lambda x: x.index, reverse=False):
        j += str(i)
        j +=","
    j = j[:-1]
    j +=']}'

    socketio.emit('edit_item_index', j, namespace='/app')
    return Response('ok', status='200')

@app.route("/edit_image", methods=['POST'])
def edit_image():

    if request.method == 'POST':

        id = request.form['id-edit']
        file_path = None
        description = request.form['description-edit']

        item = Cache.get_item(str(id))

        #check if exists
        if not item is None:
            
            file_path = -1
            #file sent.        
            if 'image-upload-edit' in request.files and request.files['image-upload-edit'].filename != '' and app.config['UPLOAD_FOLDER'] + request.files['image-upload-edit'].filename != item.file_path:
                print()
                image = request.files['image-upload-edit']
                resp = validate_image(image)
                if resp == True:
                    file_path = app.config['UPLOAD_FOLDER'] + image.filename
                else: 
                    return Response(resp, status=200)
                try:
                    os.remove(item.filename)    
                    image.save(file_path)
                except Exception as e:
                    print(str(e))
            Cache.update_item(id =str(id), file_path=file_path, description=description, status = 2)

        socketio.emit('edit_item', json.dumps({'id': item.id, 'file_path': item.file_path, 'description': item.description}) ,namespace='/app')
        return Response('200', status=200, headers={'ContentType':'application/json'})


@app.route("/add_image", methods=['POST'])
def add_image():

    if request.method == 'POST':

        #Not file sent.
        if 'image-upload' not in request.files:
            return Response('0', status=200)

        image = request.files['image-upload']
        
        #check if image is correct
        resp = validate_image(image)
        if resp == True: 

            try:
                filename = app.config['UPLOAD_FOLDER'] + image.filename    
                new_item = Item(request.form['description'], filename, request.form['index'])
                Cache.add_item(new_item.id, new_item)
            except Exception as e:
                print(str(e))
        else:
            return Response(resp, status = 200)

        socketio.emit('add_item', json.dumps({'id': new_item.id, 'file_path': new_item.file_path, 'description': new_item.description}) ,namespace='/app')
        return Response('200', status=200)

#Thread to update items to database from cache
def update_cache():
    while True:
        Time.sleep(CONSTANTS.TIME_TO_PERSIST_CACHE)

        if len(Cache.list_items) > 0 and Cache.needs_update:
            try:
                Cache.update_items()        
            except Exception as e:
                print(str(e))

def validate_image(image):
    #Check if extension is allowed
    root, ext = os.path.splitext(image.filename)

    if not ext in CONSTANTS.ALLOWED_EXTENSION:
        return '1'   

    #Check if File already exists
    filename = app.config['UPLOAD_FOLDER'] + image.filename
    if os.path.isfile(filename):
        return '3'

    #Chech image dimensions
    try: 
        image.save(filename)
        im = Image.open(image)
        w,h = im.size
        if w != CONSTANTS.WIDTH and h != CONSTANTS.HEIGHT:
            os.remove(filename)
            return '2'
    except Exception as e:
        print(str(e))
    
    return True


@socketio.on('connect', namespace='/app') 
def connect(): 
    print("***********************")
    print("*** CLIENT CONNECTED **")
    print("***********************")



################################
  #START THE APP
###############################
if __name__ == "__main__":
    app.secret_key = ''
    app.config['UPLOAD_FOLDER'] = CONSTANTS.UPLOADER_FOLDER

    t = threading.Thread(target=update_cache)
    t.start()

    Cache.get_items_from_db()

    socketio.run(app, host='0.0.0.0', debug=False, use_reloader=False) 

