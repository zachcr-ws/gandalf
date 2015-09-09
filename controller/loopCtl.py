#coding: utf-8
from config import config
import datetime
import nsqHelper
import requests
import common
import addCtl
import updateCtl
import time
import json
import md5

def loop():
    result = []
    cursor = config.mongo.find("tasks", {"status" : 1})
    for i in cursor:
        launchKeeper(i)

def launchKeeper(data):
    if data["launch_type"] == "now":
        launchOnce(data)
    elif data["launch_type"] == "schedule":
        now_unix = time.mktime(datetime.datetime.now().timetuple())
        now_date = common.unix2date( now_unix, "%Y-%m-%d %H:%M:%S" )
        if now_date == data["date"]:
            launchOnce(data)
    else:
        launchDelay(data)

def launchOnce(data):
    launch(data)
    updateCtl.updateTask(data)

def launchDelay(data):
    now_date = datetime.datetime.now()
    cron_arr = data["crontab"].split(" ")
    if (cron_arr[0] == "*" or int(cron_arr[0]) == now_date.minute) and (cron_arr[1] == "*" or int(cron_arr[1]) == now_date.hour) and (cron_arr[2] == "*" or int(cron_arr[2]) == now_date.day) and (cron_arr[3] == "*" or int(cron_arr[3]) == now_date.month) and (cron_arr[4] == "*" or int(cron_arr[4]) == now_date.weekday() + 1):
       launch(data)

def launch( data ):
    error = False
    content = ""
    hexId = common.md5String( str(data["_id"]) )
    if data["task_type"] == "post" or data["task_type"] == "get":
        if data["task_type"] == "get":
            try:
                url = common.getUrlHandler(data["address"], {"logid": hexId})
                r = requests.get(url)
                content = json.dumps(r.text)
            except Exception, ex:
                content = "\"http get error\" " + str(Exception)+":"+str(ex)
                error = True
        elif data["task_type"] == "post":
            jsonData = json.loads(data['args'])
            try:
                jsonData["logid"] = hexId
                r = requests.post(data["address"], data=jsonData)
                content = json.dumps(r.text)
            except Exception, ex:
                content = "\"http get error\" " + str(Exception)+":"+str(ex)
                error = True
    else:
        nsqHelper.nsqProductor(hexId, data["handler"], data["command"])
        content = "\"nsq send success\""

    addCtl.addLog(data, hexId, content, error)