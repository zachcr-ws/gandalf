#coding: utf-8
import tornado.web as web
from controller import indexCtl, addCtl, getlistCtl, deleteCtl, turnCtl, updateCtl, loopCtl
from config import config
from raven.contrib.tornado import AsyncSentryClient
import os
import db

#connect db
Mongo = db.MongoDB(config.mongo)
DB = Mongo.getDB()

def loopTask():
    loopCtl.loop(Mongo)
 
class IndexHandler(web.RequestHandler):
    def get(self):
        indexCtl.index(self, DB)
class AddHandler(web.RequestHandler):
    def post(self):
        addCtl.add(self, DB)
class TasklistHandler(web.RequestHandler):
    def get(self):
        getlistCtl.index(self, Mongo)
class TaskHandler(web.RequestHandler):
     def get(self):
        getlistCtl.getById(self, Mongo)
class DeleteTaskHandler(web.RequestHandler):
    def post(self):
        deleteCtl.deleteById(self, DB)
class TurnTaskHandler(web.RequestHandler):
    def post(self):
        turnCtl.turn(self, Mongo)
class UpdateHandler(web.RequestHandler):
    def post(self):
        updateCtl.update(self, Mongo)
class LogContentHandler(web.RequestHandler):
    def get(self):
        updateCtl.updateLogContent(self, Mongo)
class LogStatusHandler(web.RequestHandler):
    def get(self):
        updateCtl.updateLogStatus(self, Mongo)
class GetLogHandler(web.RequestHandler):
    def get(self):
        getlistCtl.getLog(self, Mongo)

handler = [
    (r"/", IndexHandler),
    (r"/add", AddHandler),
    (r"/getList", TasklistHandler),
    (r"/delete", DeleteTaskHandler),
    (r"/turn", TurnTaskHandler),
    (r"/getListById", TaskHandler),
    (r"/update", UpdateHandler),
    (r"/addContent", LogContentHandler),
    (r"/logStatus", LogStatusHandler),
    (r"/getLog", GetLogHandler)
]

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static") 
}

application = web.Application(handler, **settings)