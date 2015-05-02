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

#Sensor serial and its description
SENSOR1_SERIAL = '28-000006574c70'
SENSOR_TYPE = 'Temperature'

SENSOR2_SERIAL = '28-0000069885c5'
 
SENSOR3_SERIAL = '28-0000069885c4'
 
SENSOR4_SERIAL = '28-0000069885c2'
 
SENSOR5_SERIAL = '28-0000069885c3'
 
SENSOR6_SERIAL = '28-0000069885c1'

con = db.connect(DB_NAME)    
    
with con:
    cur = con.cursor()
    
#     cur.execute("""DROP TABLE IF EXISTS raspberry""")
    cur.execute("""DROP TABLE IF EXISTS sensor""")
    cur.execute("""DROP TABLE IF EXISTS data""")
    
#     cur.execute('''CREATE TABLE raspberry 
#                  (serial int)''')
#     cur.execute('''CREATE TABLE sensor
#                  (serial text, type varchar(100), pi_id int)''')

    cur.execute('''CREATE TABLE sensor
                 (serial text, type varchar(100))''')
     
    cur.execute('''CREATE TABLE data
                 (time text, depth double, value text, sensor_id text)''')
    
#     cur.execute("INSERT INTO raspberry VALUES (1)")

    cur.execute("INSERT INTO sensor VALUES ('28-0000069885c5','Temperature')")        
    cur.execute("INSERT INTO data VALUES ('02/14/15 15:05:45',10.0, '22.812','28-0000069885c5')") 
    cur.execute("INSERT INTO data VALUES ('02/14/15 15:15:45',20.0, '24.812','28-0000069885c5')")    
    cur.execute("INSERT INTO data VALUES ('02/14/15 15:25:45',30.0, '26.812 23.156','28-0000069885c5')") 

    cur.execute("""INSERT INTO sensor VALUES (?,?)""",(SENSOR1_SERIAL, SENSOR_TYPE))        
    cur.execute("INSERT INTO data VALUES ('02/14/15 15:05:45',10.0, '22.812','28-000006574c70')") 
    cur.execute("INSERT INTO data VALUES ('02/14/15 15:15:45',20.0, '24.812','28-000006574c70')")    
    cur.execute("INSERT INTO data VALUES ('02/14/15 15:25:45',30.0, '26.812 23.156','28-000006574c70')") 

#     cur.execute("""INSERT INTO data VALUES (?,?, ?, ?)""", ('02/14/15 15:05:45',10.0,'22.812',SENSOR1_SERIAL)) 
#     cur.execute("""INSERT INTO data VALUES (?,?, ?, ?)""", ('02/14/15 15:05:45',20.0,'25.0 24.123',SENSOR1_SERIAL)) 
#     cur.execute("""INSERT INTO data VALUES (?,?, ?, ?)""", ('02/14/15 15:05:45',30.0,'29.8 21.123',SENSOR1_SERIAL)) 

#     cur.execute("INSERT INTO sensor VALUES ('28-0000069885c4','Temperature', 1)") 
#     cur.execute("INSERT INTO data VALUES ('02/14/15 15:05:45',10.0, '22.812 21.12','28-0000069885c4')") 
#     cur.execute("INSERT INTO data VALUES ('02/14/15 15:15:45',20.0, '24.812','28-0000069885c4')")    
#     cur.execute("INSERT INTO data VALUES ('02/14/15 15:25:45',30.0, '26.812','28-0000069885c4')") 

    cur.execute("""INSERT INTO sensor VALUES (?,?)""",(SENSOR3_SERIAL, SENSOR_TYPE))        
    cur.execute("INSERT INTO data VALUES ('02/14/15 16:05:45',10.0, '22.812 21.12','28-0000069885c4')") 
    cur.execute("INSERT INTO data VALUES ('02/14/15 16:15:45',20.0, '24.812 22.12','28-0000069885c4')")    
    cur.execute("INSERT INTO data VALUES ('02/14/15 16:25:45',30.0, '26.812 24.12','28-0000069885c4')") 
    
#     cur.execute("INSERT INTO sensor VALUES ('28-0000069885c2','Temperature', 1)")
#     cur.execute("INSERT INTO data VALUES ('02/14/15 15:05:45',10.0, '22.812 21.12','28-0000069885c2')") 
#     cur.execute("INSERT INTO data VALUES ('02/14/15 15:15:45',20.0, '24.812','28-0000069885c2')")    
#     cur.execute("INSERT INTO data VALUES ('02/14/15 15:25:45',30.0, '26.812','28-0000069885c2')")    

    cur.execute("""INSERT INTO sensor VALUES (?,?)""",(SENSOR4_SERIAL, SENSOR_TYPE))        
    cur.execute("INSERT INTO data VALUES ('02/14/15 15:05:45',10.0, '22.812 21.12','28-0000069885c2')") 
    cur.execute("INSERT INTO data VALUES ('02/14/15 15:15:45',20.0, '24.812','28-0000069885c2')")    
    cur.execute("INSERT INTO data VALUES ('02/14/15 15:25:45',30.0, '26.812','28-0000069885c2')")    
    
#     cur.execute("INSERT INTO sensor VALUES ('28-0000069885c3','Temperature', 1)")
#     cur.execute("INSERT INTO sensor VALUES ('28-0000069885c1','Temperature', 1)")     

    cur.execute("""INSERT INTO sensor VALUES (?,?)""",(SENSOR5_SERIAL, SENSOR_TYPE))        
    cur.execute("""INSERT INTO sensor VALUES (?,?)""",(SENSOR6_SERIAL, SENSOR_TYPE))                   

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