#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

# send_data.py
#
#   Fabricio Goncalves, 18/4/2015, v1.0
#
#   Sends data to the web server database encoded in a JSON format
#   
#
#   Code is based on turorials and specifications from:
#       https://docs.python.org/2/library/httplib.html
#       http://www.anthonydebarros.com/2012/03/11/generate-json-from-sql-using-python/ 
#       https://docs.python.org/2/library/sqlite3.html
#       https://docs.python.org/2/library/logging.html

# Collections library
import collections

# Http request and json Libraries
import httplib
import json

# Sqlite Library - Accessing data in the raspberry pi 
import sqlite3 as db

# Logging Library
import logging

#Raspberry ID
RASPBERRY_ID = 1

#SQLite database name
DB_NAME = 'temperature.db'

#Log file path
LOGFILE_PATH = 'ELSpring2015/code/project/log_file.log'

# It checks if there is any row in the the data table 
def getRow():
    con = db.connect(DB_NAME)
    
    # This enables column_name
    con.row_factory = db.Row
    
    with con:
        cur = con.cursor()
        
        cur.execute("""SELECT count(*) FROM data LIMIT 1""")
        #cur.execute("""SELECT count(*) FROM dummy""")
        count = cur.fetchone()
    
    return count[0]

# It returns the sensors' serials used in the buoy 
def getSensors():
    con = db.connect(DB_NAME)
        
    with con:
        cur = con.cursor()
        
        cur.execute("""SELECT serial FROM sensor""")
        
        sensors = cur.fetchall()
    
    return sensors

# It returns the data for each sensor attached on the buoy
def getData(serial):
    con = db.connect(DB_NAME)
    
    # This enables column_name
    con.row_factory = db.Row
    
    with con:
        cur = con.cursor()
        
        cur.execute("""SELECT time, depth, value FROM data WHERE sensor_id = (?)""", (serial))
        #cur.execute("""SELECT * FROM dummy""")
        data = cur.fetchall()
    
    return data

# It deletes all the rows from the data table
def deleteRows():
    con = db.connect(DB_NAME)
        
    with con:
        cur = con.cursor()
        
        #cur.execute("""DELETE FROM data""")
        #cur.execute("""DELETE FROM dummy""")
        con.commit()
    
# It defines the JSON format to send the POST request to the server    
def defineJSON(object_list):
    
#     rows = [dict(rec) for rec in recs ]
#         
#     objects_list = []
#     
#     a = collections.OrderedDict()
#     a['serial'] = SENSOR_SERIAL
#     a['data'] = rows
#     objects_list.append(a)
    
    objects_list1 = []
    
    b = collections.OrderedDict()
    b['id'] = RASPBERRY_ID
    b['sensors'] = objects_list
    
    objects_list1.append(b)
            
    js = json.dumps(objects_list1[0])
    
    return js

# It sends the data to the web server
def sendData(json):
    
    httpServ = httplib.HTTPConnection("cs.newpaltz.edu")
    
    httpServ.connect()
    
    #http:/~fernandi2/EL2015/services/senddata.php | /~fernandi2/playground/t1.php
    httpServ.request('POST', "/~fernandi2/playground/t1.php", json)
    
    response = httpServ.getresponse()
        
    httpServ.close()
        
    return response.read()

# Main routine
#

# create logger
logger = logging.getLogger('log_file')
logger.setLevel(logging.DEBUG)

# create file handler and set level to debug
ch = handler = logging.FileHandler(filename=LOGFILE_PATH, mode='a')
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# 'application' code
#logger.debug('debug message')
#logger.info('info message')
#logger.warn('warn message')
#logger.error('error message')
#logger.critical('critical message')
     
if getRow() != 0:         

    sensors = getSensors();
    
    # Create a list to store the records for each sensor
    objects_list = []
    
    # Take the data linked to each sensor serial
    for sensor in sensors:

        recs = getData(sensor)
        
        # Skip to the other sensor if there is not any data linked to the actual sensor - No records
        if not recs:
            continue
        
        #rows = [dict(rec) for rec in recs ]
        a = collections.OrderedDict()
        obj_list = []
        
        # Uses OrderedDict() object to build a list of dictionaries
        # with each row in the database becoming one dictionary and 
        # each field in the row a key-value pair 
        for row in recs:
            d = collections.OrderedDict()
            d['time'] = row[0]
            d['depth'] = row[1]
            d['value'] = [float(n) for n in row[2].split()]
            obj_list.append(d)
        
        a['serial'] = sensor[0]
        a['data'] = obj_list
        objects_list.append(a)
    
#   recs = getData(serial)
        
    js = defineJSON(objects_list)
        
    response = sendData(js)
    
    # Converts web server's response to real json
    #response = response.replace("'", "\"") 
    
    #response_json = json.loads(response)

    if response != None: #response_json['success']:
        #deleteRows()
        #print "Data sent! \nRows deleted!"
        logger.info("Successful Transmission!")
        print response
        
    else:
        
        print "Unsuccessful Transmission! \nError: " + response_json['message'] 
        logger.error("Unsuccessful Transmission: " + response_json['message'])
    
else:
    
    print "Empty table!"
    logger.warning("Empty table!")