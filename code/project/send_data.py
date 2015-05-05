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
#       https://docs.python.org/2/library/json.html
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

#Web Server that will receive the data
WEBSERVER_HOSTNAME = 'cs.newpaltz.edu'
WEBSERVER_PATH = '/~fernandi2/EL2015/services/senddata.php'     #http:/~fernandi2/EL2015/services/senddata.php | /~fernandi2/playground/t1.php

#Log file path
LOGFILE_PATH = 'ELSpring2015/code/project/log_file.log'

# It checks if there is any row in the the data table 
def getRow():
    con = db.connect(DB_NAME)
        
    with con:
        cur = con.cursor()
        
        cur.execute("""SELECT count(*) FROM data LIMIT 1""")

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
        
    with con:
        cur = con.cursor()
        
        cur.execute("""SELECT time, depth, value FROM data WHERE sensor_id = (?)""", (serial))

        data = cur.fetchall()
    
    return data

# It deletes all the rows from the data table
def deleteRows(last_row):
    con = db.connect(DB_NAME)
        
    with con:
        cur = con.cursor()
        
        sql = "DELETE FROM data WHERE time <= " + last_row
        
        cur.execute(sql)

        con.commit()
    
# It defines the JSON format to send the POST request to the server    
def defineJSON(object_list):
    
    objects_list1 = []
    
    b = collections.OrderedDict()
    b['id'] = RASPBERRY_ID
    b['sensors'] = objects_list
    
    objects_list1.append(b)
            
    js = json.dumps(objects_list1[0])
    
    return js

# It sends the data to the web server
def sendData(json):
    
    httpServ = httplib.HTTPConnection(WEBSERVER_HOSTNAME)

    httpServ.connect()
        
    httpServ.request('POST', WEBSERVER_PATH, json)
    
    response = httpServ.getresponse()
        
    httpServ.close()
        
    return response.read()

# Main routine

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
     
# If there is any row in the data table, transmit the data
if getRow() != 0:         
    
    # Variable to store the sensors' serials
    sensors = getSensors();
    
    # Create a list to store the records for each sensor
    objects_list = []

    # Create a list to store the time from each sensor
    time_list = []

    # Take the data linked to each sensor serial
    for sensor in sensors:
        
        # Variable to store the data linked to the current sensor serial
        recs = getData(sensor)
        
        # Skip to the other sensor if there is not any data linked to the actual sensor - No records
        if not recs:
            continue

        # Create an empty dictionary to encode the JSON format        
        a = collections.OrderedDict()
        obj_list = []
        
        # Uses OrderedDict() object to build a list of dictionaries
        # with each row in the database becoming one dictionary and 
        # each field in the row a key-value pair 
        for row in recs:
            d = collections.OrderedDict()
            d['time'] = row[0]
            time_list.append(d['time'])
            d['depth'] = row[1]
            d['value'] = [float(n) for n in row[2].split()]
            obj_list.append(d)
        
        a['serial'] = sensor[0]
        a['data'] = obj_list
        objects_list.append(a)
    
    # It stores the last reading ocurred
    last_row =  max(time_list)
                
    # Variable to hold the final JSON formart that will be sent to the web server
    js = defineJSON(objects_list)
         
    # Web Server response
    response = sendData(js)
     
    # Converts web server's response to real json
    response = response.replace("'", "\"") 
     
    # Converts the json response back into python dictionary 
    response_json = json.loads(response)
 
    # If the transmission was successful
    if response_json['success']:
         
        # Delete rows from the data table
        deleteRows(last_row)
 
        # Report the event occured into the log file
        logger.info("Successful Transmission!")
        #print response
 
    # If it failed        
    else: 
         
        # Report the event occurred into the log file
        #print "Unsuccessful Transmission! \nError: " + response_json['message'] 
        logger.error("Unsuccessful Transmission: " + response_json['message'])

# If any record is stored in the table     
else:

    # Report the event occured into the log file    
    #print "Empty table!"
    logger.warning("Empty table!")