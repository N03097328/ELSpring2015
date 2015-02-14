#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask, render_template
import os
import time

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

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