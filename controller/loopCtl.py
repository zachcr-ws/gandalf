#coding: utf-8
import datetime
import nsqHelper
import requests
import common
import addCtl
import updateCtl
import time
import json
import md5

def loop(Mongo):
    result = []
    cursor = Mongo.getDbData("tasks", {"status" : 1})
    for i in cursor:
        launchKeeper(i, Mongo)

def launchKeeper(data, Mongo):
    if data["launch_type"] == "now":
        launchOnce(data, Mongo)
    elif data["launch_type"] == "schedule":
        now_unix = time.mktime(datetime.datetime.now().timetuple())
        now_date = common.unix2date( now_unix, "%Y-%m-%d %H:%M:%S" )
        if now_date == data["date"]:
            launchOnce(data, Mongo)
    else:
        launchDelay(data, Mongo)

def launchOnce(data, Mongo):
    launch(data, Mongo)
    updateCtl.updateTask(data, Mongo)

def launchDelay(data, Mongo):
    now_date = datetime.datetime.now()
    cron_arr = data["crontab"].split(" ")
    if (cron_arr[0] == "*" or int(cron_arr[0]) == now_date.minute) and (cron_arr[1] == "*" or int(cron_arr[1]) == now_date.hour) and (cron_arr[2] == "*" or int(cron_arr[2]) == now_date.day) and (cron_arr[3] == "*" or int(cron_arr[3]) == now_date.month) and (cron_arr[4] == "*" or int(cron_arr[4]) == now_date.weekday() + 1):
       launch(data, Mongo)

def launch( data, Mongo ):
    error = False
    content = ""
    hexId = common.md5String( str(data["_id"]) )
    if data["task_type"] == "post" or data["task_type"] == "get":
        if data["task_type"] == "get":
            try:
                url = common.getUrlHandler(data["address"], {"logid": hexId})
                r = requests.get(url)
                content = json.dumps(r.text)
            except:
                content = "\"http get error\""
                error = True
        elif data["task_type"] == "post":
            jsonData = json.loads(data['args'])
            try:
                jsonData["logid"] = hexId
                r = requests.post(data["address"], data=jsonData)
                content = json.dumps(r.text)
            except:
                content = "\"http post error\""
                error = True
    else:
        nsqHelper.nsqProductor(hexId, data["handler"], data["command"])
        content = "\"nsq send...\""

    addCtl.addLog(data, hexId, content, error, Mongo)