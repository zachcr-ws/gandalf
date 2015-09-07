import os

mongo = {
    "hosts" : os.environ.get("MONGO_RS_PORT_27017_TCP_ADDR") + ":27017",
    "db" : "gandalf"
}

nsq = {
    "nsq_writer_url" : "nsqd.curio.im:4150",
    "nsq_reader_url" : "nsqd.curio.im:4150"
}

#gobal nsq writer and reader
nsq_writer = ""
nsq_reader = ""
nsq_message = ""