#coding: utf-8
from bson.objectid import ObjectId
import json

def deleteById(obj, db):
    col = db["tasks"]
    taskId = obj.get_argument("id")

    code = 400
    if taskId:
        result = col.remove({"_id": ObjectId(taskId)})
        if result["n"] == 1 and result["ok"] == 1:
            code = 200
    obj.set_header("Content-Type", "text/plain")
    obj.write(json.dumps({"code": code}))