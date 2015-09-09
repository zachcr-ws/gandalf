#coding: utf-8
import tornado
import datetime
import time
import response
from config import config

def add(obj):
    data = tornado.escape.json_decode(obj.request.body)
    if("name" not in data or "task_type" not in data or "launch_type" not in data):
        response.Response(obj, 201, "Missing Argments")

    data["status"] = 0
    data["create_time"] = time.mktime(datetime.datetime.now().timetuple())
    task_id = config.mongo.insert("tasks", data)
    if task_id:
        response.Response(obj, 200, "success", str(task_id))
    else:
        response.Response(obj, 202, "Insert Error")

def addLog(task, logid, content, error):
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
    elif error == False:
        data["status"] = "success"
    data["content"] = '{"1":' + content + '}'

    config.mongo.insert("log", data)