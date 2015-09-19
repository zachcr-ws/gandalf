#coding: utf-8 
import pymongo
from config import config
from pymongo import MongoClient, ReadPreference

direction = {}
direction["ASC"] = pymongo.ASCENDING
direction["DESC"] = pymongo.DESCENDING

class MongoDSL:
    def __init__(self):
        self.Mongo = MongoDB(config.mongoConfig)
        self.DB = self.Mongo.getDB()
    
    def insert(self, name, data):
        col = self.DB[name]
        return col.insert(data)

    def count(self, name, query):
        col = self.DB[name]
        return col.count(query)

    def delete(self, name, query):
        col = self.DB[name]
        return col.remove(query)

    def find(self, name, query={}, sfield="", sortcending="DESC", limit="", skip=""):
        col = self.DB[name]
        cursor = col.find(query)
        if sfield != "":
            cursor = cursor.sort(sfield, direction[sortcending])
        if limit != "" and skip != "":
            cursor = cursor.limit(limit).skip(skip)
        return cursor

    def findOne(self, name, query):
        col = self.DB[name]
        return col.find_one(query)

    def update(self, name, query, data):
        col = self.DB[name]
        return col.update(query, {"$set": data})

    def __destory__(self):
        self.Mongo.disconnect()

class MongoDB:

    def __init__(self, c):
        self.client = MongoClient( c['hosts'] )
        self.db = self.client[c['db']]
        if config.mongoUser["user"] != "":
            self.db.authenticate(config.mongoUser["user"], config.mongoUser["password"]) 

    def getDB(self):
        return self.db

    def disconnect(self):
        self.client.close()