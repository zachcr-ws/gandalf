#coding: utf-8
import tornado
import datetime
import time
import json

def add(obj, db):
    result = ""
    col = db["tasks"]
    data = tornado.escape.json_decode(obj.request.body)
    if("name" not in data or "task_type" not in data or "launch_type" not in data):
        result = {
            "code" : "400",
            "msg" : "Missing Argments"
        }

    data["status"] = 0
    data["create_time"] = time.mktime(datetime.datetime.now().timetuple())
    task_id = col.insert(data)

    if(task_id):
        result = {
            "code" : "200",
            "msg" : str(task_id)
        }
    else:
        result = {
            "code" : "401",
            "msg" : "Insert Error"
        }

    obj.set_header("Content-Type", "text/plain")
    obj.write(json.dumps(result))

def addLog(task, logid, content, error, Mongo):
    col = Mongo.getDB()["tasks_log"]
    data = {}
    data["logid"] = logid
    data["name"] = task["name"]
    data["task_id"] = task["_id"]
    data["task_type"] = task["task_type"]
    data["launch_type"] = task["launch_type"]
    data["start_time"] = time.mktime(datetime.datetime.now().timetuple())
    data["end_time"] = ""
    data["status"] = "launching"
    if error:
        data["end_time"] = time.mktime(datetime.datetime.now().timetuple())
        data["status"] = "fail"
    elif error == False and (data["task_type"] == "get" or data["task_type"] == "post"):
        data["status"] = "success"
    data["content"] = '{"1":' + content + '}'

    log_id = col.insert(data)