from time import mktime
from datetime import datetime

def conv_1(dateTuple):
    date, hour = dateTuple.split(" ")
    year,month,day = date.split("-")
    hour,minutes = hour.split(":")

    dateTime = datetime(int(year),int(month),int(day),int(hour),int(minutes))
    return int(mktime(dateTime.timetuple()))

def conv_2(dateTuple):
    return int(dateTuple)/100

def conv_3(dateTuple):
    date, hour = dateTuple.split("T")
    year,month,day = date.split("-")
    hour,minutes,seconds = hour.split(":")

    dateTime = datetime(int(year),int(month),int(day),int(hour),int(minutes),int(seconds))
    return int(mktime(dateTime.timetuple()))

class DateConvertor():
    def __init__(self):
        self.DateFormats = {'yyyy-mm-dd hh:mm': conv_1,
        'unix_milli': conv_2,
        'yyyy-mm-ddThh:mm:ss': conv_3}

    def verifyDateFormat(self,moduleDateFormat):
        for dateFormat in self.DateFormats:
            if(moduleDateFormat == dateFormat):
                return True
        return False

    def convert(self, moduleDateFormat, dateTuple):
                return self.DateFormats[moduleDateFormat](dateTuple)
