#coding: utf-8
import tornado.template as template

def index(obj):
    loader = template.Loader("static")
    obj.write(loader.load("index.html").generate())