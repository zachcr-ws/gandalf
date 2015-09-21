#coding: utf-8
from bson.objectid import ObjectId
import response
import time
import datetime

from config import config

def getOneTaskLog(obj):

    code = 200
    limit = 10
    msg = "success"
    result = []

    tid = obj.get_argument("id")
    limit = int(obj.get_argument("limit"))

    if tid:
        cursor = config.mongo.find("log", {"task_id": ObjectId(tid)}, "start_time", "DESC", limit, 0)
        for i in cursor:
            i["_id"] = str(i["_id"])
            i["task_id"] = str(i["task_id"])
            i["start_time"] = int(i["start_time"])
            i["end_time"] = int(i["end_time"])
            result.append(i)
    else:
        code = 201
        msg = "Need Id"
    response.Response(obj, code, msg, result)

def getOverview(obj):

    logs = []
    tasks = []

    fail = config.mongo.count("log", {"status": "fail"})
    success = config.mongo.count("log", {"status": "success"})
    tasksNum = config.mongo.count("tasks", {"status": 1})
    allTask = config.mongo.count("tasks", {})

    cursor = config.mongo.find("log", {}, "start_time", "DESC", 30, 0)
    for i in cursor:
            i["_id"] = str(i["_id"])
            i["task_id"] = str(i["task_id"])
            logs.append(i)

    cursor = config.mongo.find("tasks", {"status": 1}, "create_time", "DESC", 100, 0)
    for i in cursor:
        i["_id"] = str(i["_id"])
        tasks.append(i)

    result = {
        "fail": fail,
        "success": success,
        "tasks_launching_num": tasksNum,
        "all_task": allTask,
        "launching_tasks": tasks,
        "logs": logs
    }
    response.Response(obj, 200, "success", result)
