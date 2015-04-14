#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import os
import time

#Sqlite Library - Accessing data in the raspberry pi 
import sqlite3 as db
import sys

con = db.connect('temperature.db')    
    
with con:
    cur = con.cursor()
    
    cur.execute("""DROP TABLE IF EXISTS raspberry""")
    cur.execute("""DROP TABLE IF EXISTS sensor""")
    cur.execute("""DROP TABLE IF EXISTS data""")
    cur.execute("""DROP TABLE IF EXISTS dummy""")    
    
    cur.execute('''CREATE TABLE raspberry 
                 (serial int)''')
    cur.execute('''CREATE TABLE dummy 
                 (serial int)''')    
    cur.execute('''CREATE TABLE sensor
                 (serial text, type varchar(100), pi_id int)''')
    cur.execute('''CREATE TABLE data
                 (time text, depth double, value double, sensor_id text)''')
    
    cur.execute("INSERT INTO raspberry VALUES (1)")
    cur.execute("INSERT INTO dummy VALUES (1)")
    cur.execute("INSERT INTO sensor VALUES ('28-0000069885c5','Temperature', 1)") 
    cur.execute("INSERT INTO data VALUES ('02/14/15 15:05:45',10.0, 22.812,'28-0000069885c5')") 
    cur.execute("INSERT INTO data VALUES ('02/14/15 15:15:45',20.0, 24.812,'28-0000069885c5')")    
    cur.execute("INSERT INTO data VALUES ('02/14/15 15:25:45',30.0, 26.812,'28-0000069885c5')") 
       
    con.commit()
                           
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