#coding: utf-8
from config import config
import nsq
import json

def nsqProductor(id, handler, command):
    topic = "Nsq-Curio-Task"
    if handler != "":
        topic = handler

    data = {
        "logid" : id,
        "data" : command
    }
    
    data = json.dumps(data)
    writer = config.nsq_writer
    writer.pub(str(topic), str(data), nsqCallback)

def nsqCallback(conn, data):
    config.nsq_message = str(conn) + " : " + str(data)