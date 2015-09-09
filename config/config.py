import os

mongoConfig = {
    "hosts" : os.environ.get("MONGO_RS_PORT_27017_TCP_ADDR") + ":27017",
    "db" : "gandalf"
}

nsq = {
    "nsq_writer_url" : "192.168.5.2:4150",
    "nsq_reader_url" : "192.168.5.2:4150"
}

#gobal nsq writer and reader
nsq_writer = ""
nsq_reader = ""
nsq_message = ""

#gobal mongo object
mongo = ""