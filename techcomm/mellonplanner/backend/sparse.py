'''
Created on Mar 21, 2015

@author: Bill
'''

import urllib2
import re
from clslecrec import Cls, Lec, Rec, getDay

import time

BASE_URL = "https://enr-apps.as.cmu.edu/assets/SOC/"
URL_SUFFIXES = ['sched_layout_fall.htm',
                'sched_layout_spring.htm',
                'sched_layout_summer_1.htm',
                'sched_layout_summer_2.htm']

INDEX = {  'blank':0,
           'id':1,
           'name':2,
           'units':3,
           'lecsec':4,
           'days':5,
           'timestart':6,
           'timeend':7,
           'room':8,
           'location':9,
           'instructors':10}

LINE_SPLIT_RE = r'<TR><TD.*?>|<TD.*?>|</TD><TD.*?>|</TD></TR>'
LEC_RE = r'Lec\w*\d*'


def parseTime(timeStr):
    #parse time format HH:MM(AM/PM)
    hr = int(timeStr[:-5])
    minute = round(float(timeStr[-4:-2])/60.0 * 2)/2.0
    ampm = timeStr[-2:]
    if ampm.lower() == 'pm' and hr != 12:
        hr += 12
    if ampm.lower() == 'am' and hr == 12:
        hr = 0
    return hr + minute

def parseSched(f):

    sched = {}
    activeCls = None
    activeLec = None
    lecStyle = False
    activeRec = None

    allTokens = []
    i = 0
    for line in f:
        line = line.strip()
        line = line.replace('&nbsp;', '')

        tokens = re.split(LINE_SPLIT_RE, line)
        allTokens.append(tokens)

        i += 1

    # f is an html file object
    for i in range(len(allTokens)):
        tokens = allTokens[i]

        if len(tokens) >= 11:
            blank = tokens[INDEX['blank']]
            cid = tokens[INDEX['id']]
            name = tokens[INDEX['name']]
            units = tokens[INDEX['units']]
            lecsec = tokens[INDEX['lecsec']]
            days = tokens[INDEX['days']]
            timestart = tokens[INDEX['timestart']]
            timeend = tokens[INDEX['timeend']]
            location = tokens[INDEX['location']]
            instructors = tokens[INDEX['instructors']]

            cid_intq = False
            try:
                _ = int(cid)
                cid_intq = True
            except:
                pass

            units_floatq = False
            try:
                _ = float(units)
                units_floatq = True
            except:
                pass


            if re.sub(r'\s*', '', location.lower()) == '':
                #two-line name
                if not cid or (cid and cid_intq):
                    allTokens[i+1] = map(lambda (a,b): a+b, zip(tokens, allTokens[i+1]))
                continue
            else:
                pass

            if cid:
                # new class
                if activeCls:
                    sched[activeCls.cId] = activeCls
                if cid_intq:
                    activeCls = Cls(cid, int(float(units)) if units_floatq else 0)

            if 'pittsburgh' not in location.lower():
                continue

            if not timestart or not timeend or (not lecsec and not activeRec):
                continue
            timestart = parseTime(timestart)
            timeend = parseTime(timeend)

            if cid and cid_intq:
                activeLec = Lec(days, timestart, timeend)
                activeCls.lecs = {lecsec:activeLec}
                if re.match(LEC_RE, lecsec):
                    lecStyle = True
                else:
                    lecStyle = False
                activeRec = None
            elif lecsec and re.match(LEC_RE, lecsec):
                #new lecture in style "Lec..."
                lecStyle = True
                activeLec = Lec(days, timestart, timeend)
                activeCls.lecs[lecsec] = activeLec
                activeRec = None
            elif lecsec and not lecStyle:
                #new lecture in other style
                activeLec = Lec(days, timestart, timeend)
                activeCls.lecs[lecsec] = activeLec
                activeRec = None
            elif not lecsec and activeRec:
                #second recitation
                for day in days:
                    activeRec.rDays.append(getDay(day))
                activeRec = None
            elif lecsec:
                #recitation
                newRec = Rec(days, timestart, timeend)
                activeLec.recs[lecsec] = newRec
                activeRec = newRec


    return sched


def getFullSchedule(semIndex):
    url = BASE_URL + URL_SUFFIXES[semIndex]

    conn = None
    try:
        conn = urllib2.urlopen(url)
    except Exception as e:
        print("Unable to connect to %s\n%s" % (url, e))
        return None

    result = parseSched(conn)

    conn.close()

    return result

if __name__ == '__main__':
    t0 = time.clock()
    msched = getFullSchedule(0)
    print('Success .. %f' % (time.clock() - t0))
