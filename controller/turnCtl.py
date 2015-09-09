#coding: utf-8
from bson.objectid import ObjectId
from config import config
import response

def turn(obj):
    taskId = obj.get_argument("id")
    status = int(obj.get_argument("status"))
    
    code = 400
    msg = "failed"
    if taskId:
        result = config.mongo.update("tasks", {"_id": ObjectId(taskId)}, {"status" :status})    
        if result["updatedExisting"] == True and result["n"] == 1:
            code = 200
            msg = "success"
    response.Response(obj, code, msg)