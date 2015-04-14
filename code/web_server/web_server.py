#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask, render_template
from flask import request
from flask import Response
from flask import json
import os
import time

#Sqlite Library
import sqlite3 as db
import sys

app = Flask(__name__)

@app.route("/gettemp", methods = ['GET'])
def hello():
    time = float(request.args['n']) / 30
    
    con = db.connect('temperature.db')
    
    with con:
        cur = con.cursor()

        cur.execute("SELECT COUNT(*) FROM TempData ")
        
        offset = cur.fetchone()
        
        offset = float(offset[0]) - time
        
        cur.execute("""SELECT date, roomTempC, cityTempC FROM TempData LIMIT ? OFFSET ? """, (time, offset))

        data = cur.fetchall()

    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')

    return resp

@app.route("/readtemp")
def readTemp():
    tempfile = open("/sys/bus/w1/devices/28-0000069885c5/w1_slave")
    tempfile_text = tempfile.read()
    currentTime=time.strftime('%x %X %Z')
    tempfile.close()
    tempC=float(tempfile_text.split("\n")[1].split("t=")[1])/1000
    tempF=tempC*9.0/5.0+32.0
    templateData = {
      'date' : currentTime,
      'celsius': str(tempC),
      'faren': str(tempF)
      }
    return render_template('main.html', **templateData)
    #"Current Time " + currentTime + " Temperature " + str(tempC) +"°C / " + str(tempF) + "°F"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)