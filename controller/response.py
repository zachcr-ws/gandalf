#coding: utf-8
import json

def Response(obj, code, msg, data=""):
    result = {
        "code": str(code),
        "msg": msg
    }

    if data != "":
        result["data"] = data

    obj.set_header("Content-Type", "application/json")
    obj.write(json.dumps(result))