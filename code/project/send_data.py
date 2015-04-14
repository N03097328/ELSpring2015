#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import os
import time

#Http request and json Libraries
import httplib
import json

#Sqlite Library - Accessing data in the raspberry pi 
import sqlite3 as db
import sys

#MySql Library - Accsessing database server to send data
import MySQLdb

def getData():
    con = db.connect('temperature.db')
    
    # This enables column_name
    con.row_factory = db.Row
    
    with con:
        cur = con.cursor()
        
        cur.execute("""SELECT date, roomTempC, cityTempC FROM TempData LIMIT 5""")

        data = cur.fetchall()
    
    return data

recs = getData()

# for row in rows:
#     print row[0]
#     print row[1]
#     print row[2]
    
# Open database connection
#db = MySQLdb.connect(host='127.0.0.1',port=3307,user='telesduf1',passwd='',db='telesduf1_db')

# prepare a cursor object using cursor() method
#cursor = db.cursor()

httpServ = httplib.HTTPConnection("cs.newpaltz.edu")
httpServ.connect()

rows = [ dict(rec) for rec in recs ]
    
js = json.dumps(rows)
    
httpServ.request('POST', "/~fernandi2/playground/t1.php", js)
    
response = httpServ.getresponse()
#json_string = response.read().decode()
    
# Convert from json to python data
#json_data = json.loads(json_string)
        
httpServ.close()

print response.read() 
# try:
#    for row in rows:
#        # Execute the SQL command
#        sql = "INSERT INTO Temperature_Test (Date, RoomTempC, CityTempC) \
#        VALUES ('%s', '%f', '%f')" % \
#        (row[0],row[1],row[2])
#        cursor.execute(sql)        
#        # Commit your changes in the database
#        db.commit()
# except MySQLdb.Error, e:
#     try:
#         print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
#     except IndexError:
#         print "MySQL Error: %s" % e
#     # Rollback in case there is any error
#     #db.rollback()
#     print "ROLLBACK"
# # disconnect from server
# db.close()

# {
#     'id': 11111111,
#     'sensors': [
#         {
#             'serial': 'serial0000000_1',
#             'data': [
#                 {
#                     'timestamp': 321321,
#                     'depth': 12312,
#                     'data':[5]
#             ]
#         },
#         {
#             'serial': 'serial0000000_1',
#             'data': [
#                 {
#                     'timestamp': 321321,
#                     'depth': 12312,
#                     'data':[5]
#             ]
#         },
#     ]
# }