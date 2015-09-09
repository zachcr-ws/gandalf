#coding: utf-8
from bson.objectid import ObjectId
from config import config
import common
import json

def index(obj):
    result = []
    cursor = config.mongo.find("tasks")
    for i in cursor:
        data = transfer(i)
        result.append(data)
    obj.set_header("Content-Type", "text/plain")
    obj.write(json.dumps(result))

def getById(obj):
    taskId = obj.get_argument("id")
    result = []
    if taskId:
        cursor = config.mongo.find("tasks", {"_id": ObjectId(taskId)})
        for i in cursor:
            i["_id"] = str(i["_id"])
            result.append(i)
    obj.set_header("Content-Type", "text/plain")
    obj.write(json.dumps(result))

def getLog(obj):
    status = obj.get_argument("status")
    page = int(obj.get_argument("page"))
    size = int(obj.get_argument("size"))
    limit = size

    if page > 1:
        skip = (page - 1) * size
    else:
        skip = 0
    result = []
    if status:
        cursor = config.mongo.find("tasks_log", {"status": status}, "start_time", "DESC", limit, skip)
        for i in cursor:
            i["_id"] = str(i["_id"])
            i["task_id"] = str(i["task_id"])
            result.append(i)
    obj.set_header("Content-Type", "text/plain")
    obj.write(json.dumps(result))

def transfer( i ):
    i["_id"] = str(i["_id"])
    if(i["task_type"] == "shell"):
        i["task_info"] = i["handler"] + ":" + i["command"]
    else:
        i["task_info"] = i["address"] + " " + i["args"]

    if(i["launch_type"] == "schedule"):
        i["launch_time"] = "When:" + i["date"]
    elif(i["launch_type"] == "now"):
        i["launch_time"] = "Once"
    else:
        i["launch_time"] = "Corntab:" + i["crontab"]

    if i["status"] == 0:
        i["status"] = "closed"
    else:
        i["status"] = "opened"
    if "create_time" in i:
        i["create_time"] = common.unix2date(i["create_time"], "%Y-%m-%d %H:%M:%S")
    return i