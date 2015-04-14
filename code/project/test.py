#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import os
import time
import collections

#Http request and json Libraries
import httplib
import json

#Sqlite Library - Accessing data in the raspberry pi 
import sqlite3 as db
import sys

RASPBERRY_ID = 1
SENSOR_SERIAL = '28-0000069885c5'

def getRowsNumber():
    con = db.connect('temperature.db')
    
    # This enables column_name
    con.row_factory = db.Row
    
    with con:
        cur = con.cursor()
        
        cur.execute("""SELECT count(*) FROM data""")
        #cur.execute("""SELECT count(*) FROM dummy""")
        count = cur.fetchone()
    
    return count[0]

def getData():
    con = db.connect('temperature.db')
    
    # This enables column_name
    con.row_factory = db.Row
    
    with con:
        cur = con.cursor()
        
        cur.execute("""SELECT time, depth, value FROM data""")
        #cur.execute("""SELECT * FROM dummy""")
        data = cur.fetchall()
    
    return data

def deleteRows():
    con = db.connect('temperature.db')
        
    with con:
        cur = con.cursor()
        
        #cur.execute("""DELETE FROM data""")
        #cur.execute("""DELETE FROM dummy""")
        con.commit()
    
def defineJSON(recs):
    
    rows = [ dict(rec) for rec in recs ]
    
    objects_list = []
    
    a = collections.OrderedDict()
    a['serial'] = SENSOR_SERIAL
    a['data'] = rows
    objects_list.append(a)
    
    objects_list1 = []
    
    b = collections.OrderedDict()
    b['id'] = RASPBERRY_ID
    b['sensors'] = objects_list
    objects_list1.append(b)
        
    js = json.dumps(objects_list1)
    
    return js

def sendData(json):
    
    httpServ = httplib.HTTPConnection("cs.newpaltz.edu")
    
    httpServ.connect()
    
    httpServ.request('POST', "/~fernandi2/playground/t1.php", json)
    
    response = httpServ.getresponse()
        
    httpServ.close()
        
    return response.read()
    
if getRowsNumber() != 0:         

    recs = getData()
        
    js = defineJSON(recs)
        
    response = sendData(js)
        
    if response != None:
        
        #deleteRows()
        print response
        
    else:
        
        print "Unsuccessful Transmission!"
    
else:
    
    print "Empty table!"