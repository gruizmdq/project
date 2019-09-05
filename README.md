# Single Page Aplication

This is an aplication that displays a list of images with their description. It implements some features like drag and drop 

## Getting Started

Follow these steps to get a copy of the app.

### Prerequisites

```
Python 3.5 or higher
MongoDB
```

### Installing

You need to run the following commands in terminal.

This command will install the libraries needed: Flask, Pymongo and PILLOW
```
pip install requirements.txt
```

Then you should start mongod service (We assumed that mongodb is already installed)
```
sudo service mongod start
```

Now, you need to create a new DB
```
> use new_db
```

Finnaly you have to create a new collection
```
> db_createCollection('items')
```

## Before Running

Before you can run the app, you need to rename some constants. Please, go to constants.py and edit them

## Running the tests

```
> python app.py
```

## Authors

* **Gonzalo Ruiz** - 
Thank you to Eric Bidelman. For drag and drop I read his article in https://www.html5rocks.com/es/tutorials/dnd/basics/


## Considerations

For the correct working of the application, it is necessary that when "drag and drop" is made, a black border-top appears on the new location before "dropping". If it does not appear, it may "crash".

When an image file is edited, it will not be displayed to clients until they refresh the page. Only the client who made the change will see it.

To edit the time that elapses before the cache memory persists in the database, open the constants.py file 

