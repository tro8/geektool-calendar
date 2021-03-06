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


import calendar
import datetime
import re
import cal_googleapis_calendar

nocolor='\033[0m'


#
# 0 1 2 3 4 5 6
# m t w t f s s
#

# ------------------------------------------------
#
# ------------------------------------------------
def createCalendar(year, month):
    calText=calendar.TextCalendar(6)
    #    s=calText.prmonth(year,month)
    s=calText.formatmonth(year, month)

    w=s.split('\n')

    #    for i in w:
    #        print i

    #    print len(w)

    count=0
    ss = ''
    while count < len(w)-1:
    #        print ' ' + w[count] + ' '
        ss += ' ' + w[count] + ' ' + '\n'
        count += 1
    # print count, len(w)

    # p = re.compile('^')
    # s=p.sub('_', s)
    # print re.search('^.',s)

    return ss


# ------------------------------------------------
#
# ------------------------------------------------
def doToday(s, day, color):

    sday = str(day)
    s=re.sub( ' ' + sday + ' ' ,' ' +color + sday + nocolor + ' ', s)
    #s=re.sub( ' ' + sday + ' ' ,'[' +color + sday + nocolor + ']', s)
    #s=re.sub( ' ' + sday + ' ' ,'[' + sday  + ']', s)
    return s

# ------------------------------------------------
#
# ------------------------------------------------
def doHoliday(s, dayList, color):

    for day in dayList:
        sday = str(day)
        s=re.sub( ' ' + sday + ' ' ,' ' +color + sday + nocolor + ' ', s)

    return s


# ------------------------------------------------
#
# ------------------------------------------------
def doWeek(s, days, week, color):

    cal = calendar.Calendar(6)

    for i in days: #cal.itermonthdays2(2013,5):
        if i[0] > 0 and i[1]==week:
            day = str(i[0])
            s=re.sub( ' ' + day + ' ' ,' ' +color + day + nocolor + ' ', s)
    return s

# ------------------------------------------------
#
# ------------------------------------------------
def doCal(year, month, day):

    s = createCalendar(year, month)

    cal = calendar.Calendar(6)
    days1 = cal.itermonthdays2(year, month)
    days2 = cal.itermonthdays2(year, month)

    if day != 0:
        s = doToday(s, day, '\033[1;32m')

    holidayList = cal_googleapis_calendar.getHoliday(year, month)
    s = doHoliday(s, holidayList, '\033[1;31m')


    s = doWeek(s, days1, 5, '\033[1;34m')
    s = doWeek(s, days2, 6, '\033[1;31m')

    print s


# ------------------------------------------------
#
# ------------------------------------------------
if __name__ == "__main__":

    today = datetime.date.today()
    year= today.year
    month= today.month
    day=today.day

    if month - 1 == 0:
        lastYear= year - 1
        lastMonth = 12
    else:
        lastYear = year
        lastMonth = month - 1

    doCal(lastYear, lastMonth, 0)

    doCal(year, month, day)

    if month + 1 > 12:
        nextYear= year + 1
        nextMonth = 1
    else:
        nextYear = year
        nextMonth = month + 1

    doCal(nextYear, nextMonth, 0)
