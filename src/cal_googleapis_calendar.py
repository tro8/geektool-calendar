#! /usr/bin/python
#
# The MIT License (MIT)
#
# Copyright (c) 2015 tro8
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime
import httplib
import urlparse
import urllib2
import json
import os.path
import ConfigParser

cudir = os.path.abspath(os.path.dirname(__file__)) + "/"

# ------------------------------------------------
#
# ------------------------------------------------
def getUrl(day):

    year= day.year
    month= day.month

    if month+1 > 12:
        month2 = 1
        year2 = year + 1
    else:
        month2 = month + 1
        year2 = year

    day2 = datetime.date(year2, month2, 1)

    #
    inifile = ConfigParser.SafeConfigParser()
    inifile.read( cudir + "cal.ini")
    apiKey=inifile.get("calendar","apikey")

    #
    sb = "https://www.googleapis.com/calendar/v3/calendars"
    sb += "/ja.japanese%23"
    sb += "holiday@group.v.calendar.google.com/events"
    sb += "?key=" + apiKey
    sb += "&timeMin=" + str(day) + "T00:00:00Z"
    sb += "&timeMax=" + str(day2) + "T00:00:00Z"
    sb += "&maxResults=100"
    sb += "&orderBy=startTime"
    sb += "&singleEvents=true"

    # print sb

    # o=urlparse.urlparse(sb)
    # print o.geturl()

    return sb

# ------------------------------------------------
#
# ------------------------------------------------
def getData(url):

    req = urllib2.urlopen(url)
    # f=urllib2.build_opener(req)
    data=json.load(req)

    # f = open("test.txt","w")

    # print( json.dump(data,f, indent=4) )

    # f.write(data)
    # f.close()

    # print json.dumps(data, indent=4)

    return data


def toList(data):

    # f = open("test.txt","r")

    # data=json.load(f)

    datelist = []

    if data.has_key('items') == False:
        return datelist

    items = data["items"]

    for i in items:
        datelist.append(i["start"]["date"])
        # print i["start"]["date"]

    # print data["items"][0]["start"]["date"]
    #print data["items"][1]["start"]

    return datelist

# ------------------------------------------------
#
# ------------------------------------------------
def fileToList(fileName):

    f = open( cudir + fileName,"r")

    l=[]
    for i in f:
        l.append( i.replace('\n','') )

    f.close()

    return l


# ------------------------------------------------
#
# ------------------------------------------------
def fileSave(list, fileName):

    f = open( cudir + fileName, "w")

    for i in list:
        d = datetime.datetime.strptime(i, "%Y-%m-%d")
        # print d

        f.write( str(d.day) + '\n' )

    f.close()

# ------------------------------------------------
#
# ------------------------------------------------
def getHoliday(year, month):

    fileName = "cal-{}-{:02d}.txt".format(year, month)

    if os.path.exists( cudir + fileName):
        # print 'exist'
        holidays = fileToList(fileName)
    else:
        # print 'no exist'
        startDay = datetime.date(year, month, 1)
        url = getUrl(startDay)
        data = getData(url)
        holidays = toList(data)
        fileSave(holidays, fileName)

    return holidays


# ------------------------------------------------
#
# ------------------------------------------------
if __name__ == "__main__":

    today = datetime.date.today()
    year= today.year
    month= 5 #today.month

    # ------------------

    holidays=getHoliday(year, month)

    for i in holidays:
        print i
