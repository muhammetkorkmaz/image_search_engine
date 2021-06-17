import pymongo
from pymongo import MongoClient
import re

cluster=MongoClient("mongodb+srv://muho:84437**ayt@cluster0.m6sqp.mongodb.net/muho?retryWrites=true&w=majority")
db=cluster["muho"]
collection=db["images"]

def get_img_database(key):
    url_list = []
    regx = re.compile("{}".format(key), re.IGNORECASE)
    collections = collection.find({"caption": regx})
    for x in collections:
        url_list.append(x['url'])
    return url_list
liste=get_img_database("cake")
for l in liste:
    print(l)