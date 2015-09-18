#coding: utf-8
import datetime
import time
import md5
import pytz

tz = pytz.timezone(pytz.country_timezones('cn')[0])

def unix2date( t, tformat ):
    return datetime.datetime.fromtimestamp( int(t) ).strftime(tformat)

def date2unix( date, tformat ):
    return time.mktime(datetime.datetime.strptime(date, tformat).timetuple())

def md5String( code ):
    unix = time.mktime(datetime.datetime.now(tz).timetuple())
    m = md5.new()
    m.update(str(code) + ":" + str(unix))
    return m.hexdigest()

def transfer( i ):
    i["_id"] = str(i["_id"])
    return i
    
def getUrlHandler( url, param ):
    paramStr = ""
    for i in param:
        paramStr += "&" + str(i) + "=" + str(param[i])

    if '?' not in str(url):
        paramStr = paramStr.replace("&", "?", 1)

    return url + paramStr