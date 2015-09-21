#coding: utf-8
from config import config
import tornado.ioloop
import tornado.web
import router
import nsq

if __name__ == "__main__":
    #NSQ writer
    writer = nsq.Writer([config.nsq["nsq_writer_url"]])
    config.nsq_writer = writer

    router.application.listen(80)
    tornado.ioloop.PeriodicCallback(router.loopTask, 1000).start()
    tornado.ioloop.IOLoop.instance().start()
    nsq.run()