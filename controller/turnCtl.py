#coding: utf-8
from bson.objectid import ObjectId
import json

def turn(obj, Mongo):
    taskId = obj.get_argument("id")
    status = int(obj.get_argument("status"))
    
    code = 400
    if taskId:
        result = Mongo.updateDbData("tasks", {"_id": ObjectId(taskId)}, {"status" :status})    
        if result["updatedExisting"] == True and result["n"] == 1:
            code = 200
    obj.set_header("Content-Type", "text/plain")
    obj.write(json.dumps({"code": code}))