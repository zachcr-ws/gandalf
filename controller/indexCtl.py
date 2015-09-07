#coding: utf-8
import tornado.template as template

def index(obj, db):
    loader = template.Loader("static")
    obj.write(loader.load("index.html").generate())