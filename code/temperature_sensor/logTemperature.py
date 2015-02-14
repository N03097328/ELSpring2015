#!/usr/bin/python
import os
import time

#Http request and json Libraries
import httplib
import json

#Sqlite Library
import sqlite3 as db
import sys

""" Reads current Room's Temperature
    Returns Temperature in Celsius """
def roomTemp():
     tempfile = open("/sys/bus/w1/devices/28-0000069885c5/w1_slave")
     tempfile_text = tempfile.read()
     currentTime=time.strftime('%x %X')
     tempfile.close()
     tempC=float(tempfile_text.split("\n")[1].split("t=")[1])/1000
     return tempC

""" Reads current City's(New Paltz, NY) Weather 
    Returns Temperature in Celsius """
def cityTemp():
     httpServ = httplib.HTTPConnection("www.openweathermap.org")
     httpServ.connect()
        
     httpServ.request('GET', "/data/2.5/weather?q=12561,usa&units=metric")
        
     response = httpServ.getresponse()
     json_string = response.read().decode()
        
     # Convert from json to python data
     json_data = json.loads(json_string)
            
     httpServ.close()
     
     return float(json_data['main']['temp'])

""" Handles Celsius to Fahrenheit conversion 
    Returns Temperature in Fahrenheit """
def convertCtoF(tempC):
     return tempC*9.0/5.0+32.0
 
""" logs the temperature into TempData table 
    Returns string with current Fahrenheit Temperature and logged Message """ 
def logTemperature(date, roomTempC, roomTempF, cityTempC, cityTempF):
    con = db.connect('temperature.db')
    
    with con:
        cur = con.cursor()    
        cur.execute("""INSERT INTO TempData (date, roomTempC, roomTempF, cityTempC, cityTempF) 
                       VALUES(?,?,?,?,?) """, (date, roomTempC, roomTempF, cityTempC, cityTempF))        
        cur.fetchone()
        
        return "Current Temperature is: %.4f F \nTemperature logged" % roomTempF

#Main Program
date = time.strftime('%x %X')
roomTempC = roomTemp()
roomTempF = convertCtoF(roomTempC)
cityTempC = cityTemp()
cityTempF = convertCtoF(cityTempC)

print logTemperature(date, roomTempC, roomTempF, cityTempC, cityTempF)