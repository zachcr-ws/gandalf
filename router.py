#coding: utf-8
import tornado.web as web
from controller import indexCtl, addCtl, getlistCtl, deleteCtl, turnCtl, updateCtl, loopCtl, statistics
from raven.contrib.tornado import AsyncSentryClient
from config import config
import os
import db

#connect db
config.mongo = db.MongoDSL()

def loopTask():
    loopCtl.loop()
 
class IndexHandler(web.RequestHandler):
    def get(self):
        indexCtl.index(self)
class AddHandler(web.RequestHandler):
    def post(self):
        addCtl.add(self)
class TasklistHandler(web.RequestHandler):
    def get(self):
        getlistCtl.index(self)
class TaskHandler(web.RequestHandler):
     def get(self):
        getlistCtl.getById(self)
class DeleteTaskHandler(web.RequestHandler):
    def post(self):
        deleteCtl.deleteById(self)
class TurnTaskHandler(web.RequestHandler):
    def post(self):
        turnCtl.turn(self)
class UpdateHandler(web.RequestHandler):
    def post(self):
        updateCtl.update(self)
class GetLogHandler(web.RequestHandler):
    def get(self):
        getlistCtl.getLog(self)
class GetStatisticsHandler(web.RequestHandler):
    def get(self):
        statistics.getOverview(self)
class GetLogByIdHandler(web.RequestHandler):
    def get(self):
        statistics.getOneTaskLog(self)

handler = [
    (r"/", IndexHandler),
    (r"/add", AddHandler),
    (r"/getList", TasklistHandler),
    (r"/delete", DeleteTaskHandler),
    (r"/turn", TurnTaskHandler),
    (r"/getListById", TaskHandler),
    (r"/update", UpdateHandler),
    (r"/getLog", GetLogHandler),
    (r"/overview", GetStatisticsHandler),
    (r"/logs", GetLogByIdHandler)
]

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static") 
}

application = web.Application(handler, **settings)