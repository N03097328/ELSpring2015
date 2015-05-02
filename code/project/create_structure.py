#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

# create_structure.py
#
#   Fabricio Goncalves, 18/4/2015, v1.0
#
#   Creates the SQLite database structure that will store the data from the sensors 
#   

#Sqlite Library - Accessing data in the raspberry pi 
import sqlite3 as db

#SQLite database name running in the raspberry pi
DB_NAME = 'temperature.db'

#Sensor serial and its type description
SENSOR_SERIAL = '28-000006574c70'
SENSOR_TYPE = 'Temperature'

con = db.connect(DB_NAME)    
    
with con:
    cur = con.cursor()
    
    cur.execute("""DROP TABLE IF EXISTS sensor""")
    cur.execute("""DROP TABLE IF EXISTS data""")
    
    cur.execute('''CREATE TABLE sensor
                 (serial text, type varchar(100))''')
    
    cur.execute('''CREATE TABLE data
                 (time text, depth double, value text, sensor_id text)''')
    
    cur.execute("""INSERT INTO sensor VALUES (?,?)""",(SENSOR_SERIAL, SENSOR_TYPE))        

    con.commit()
                            