#coding: utf-8 
import pymongo
from pymongo import MongoClient, ReadPreference

direction = {}
#
direction["ASC"] = pymongo.ASCENDING
direction["DESC"] = pymongo.DESCENDING

class MongoDB:

    def __init__(self, config):
        self.client = MongoClient( config['hosts'] )
        self.db = self.client[config['db']]

    def getDB(self):
        return self.db

    def disconnect(self):
        self.client.close()

    def getDbData(self, name, query={}, sort_obj="", sortcending="DESC", limit="", skip=""):
        col = self.db[name]
        cursor_obj = col.find(query)
        if sort_obj != "":
            direct = direction[sortcending]
            cursor_obj = cursor_obj.sort(sort_obj, direct)
        if limit != "" and skip != "":
            cursor_obj = cursor_obj.limit(limit).skip(skip)
        return cursor_obj

    def getOne(self, name, query):
        col = self.db[name]
        return col.find_one(query)

    def updateDbData(self, name, query, data):
        col = self.db[name]
        return col.update(query, {"$set" :data})