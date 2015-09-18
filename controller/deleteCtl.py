#coding: utf-8
from bson.objectid import ObjectId
from config import config
import response

def deleteById(obj):
    taskId = obj.get_argument("id")

    code = 201
    msg = "fail"
    if taskId:
        result = config.mongo.delete("tasks", {"_id": ObjectId(taskId)})
        if result["n"] == 1 and result["ok"] == 1:
            code = 200
            msg = "success"
    response.Response(obj, code, msg)