#coding: utf-8
from bson.objectid import ObjectId
import tornado
import datetime
import time
import json

def update(obj, Mongo):
    taskId = obj.get_argument("id")
    code = 400

    if taskId:
        data = tornado.escape.json_decode(obj.request.body)
        if isinstance(data["_id"], unicode):
            data["_id"] = ObjectId(data["_id"])
        data["create_time"] = time.mktime(datetime.datetime.now().timetuple())
        result = Mongo.updateDbData("tasks", {"_id": ObjectId(taskId)}, data)
        if result["ok"] == 1 and result["n"] == 1:
            code = 200
    obj.set_header("Content-Type", "text/plain")
    obj.write(json.dumps({"code": code, "msg": taskId}))
    
#Update Log Content API, JSONP
def updateLogContent(obj, Mongo):
    logId = obj.get_argument("id")
    content = obj.get_argument("content")
    code = 400
    msg = "Error"

    if logId and content:
        log = Mongo.getOne("tasks_log", {"logid": logId})
        log['content'] = log['content'].replace('}', ', "2":"' + content + '"}')
        result = Mongo.updateDbData("tasks_log", {"logid": logId}, log)
        if result["ok"] == 1 and result["n"] == 1:
            code = 200
            msg = "Update Success"

    obj.set_header("Content-Type", "text/plain")
    obj.write('callback(' + json.dumps({"code": code, "msg": msg}) + ')')

#Update Log Status API, JSONP
def updateLogStatus(obj, Mongo):
    logId = obj.get_argument("id")
    status = obj.get_argument("status")
    code = 400
    msg = "Error"

    if logId and status:
        log = {
            "status" : status
        }
        result = Mongo.updateDbData("tasks_log", {"logid": logId}, log)
        if result["ok"] == 1 and result["n"] == 1:
            code = 200
            msg = "Update Success"

    obj.set_header("Content-Type", "text/plain")
    obj.write('callback(' + json.dumps({"code": code, "msg": msg}) + ')')

def updateTask(data, Mongo):
    taskId = data["_id"]

    if taskId:
        data["status"] = 0
        if isinstance(data["_id"], unicode):
            data["_id"] = ObjectId(data["_id"])
            taskId = data["_id"]
        result = Mongo.updateDbData("tasks", {"_id": taskId}, data)