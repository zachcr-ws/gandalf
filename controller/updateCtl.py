#coding: utf-8
from bson.objectid import ObjectId
from config import config
import tornado
import datetime
import time
import json
import response

def update(obj):
    code = 400
    msg = "fail"

    data = tornado.escape.json_decode(obj.request.body)
    if isinstance(data["_id"], unicode):
        data["_id"] = ObjectId(data["_id"])
    data["create_time"] = time.mktime(datetime.datetime.now().timetuple())
    result = config.mongo.update("tasks", {"_id": data["_id"]}, data)
    if result["ok"] == 1 and result["n"] == 1:
        code = 200
        msg = "success"

    response.Response(obj, code, msg)

def updateTask(data):
    taskId = data["_id"]

    if taskId:
        data["status"] = 0
        if isinstance(data["_id"], unicode):
            data["_id"] = ObjectId(data["_id"])
            taskId = data["_id"]
        result = config.mongo.update("tasks", {"_id": taskId}, data)