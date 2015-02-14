import httplib
import urllib
import json
import time

def printText(txt):
    lines = txt.split('\n')
    for line in lines:
        print line.strip()

httpServ = httplib.HTTPConnection("www.openweathermap.org")
httpServ.connect()

httpServ.request('GET', "/data/2.5/weather?q=12561,usa&units=metric")

response = httpServ.getresponse()
json_string = response.read().decode()

# Convert from json to python data
json_data = json.loads(json_string)

if response.status == httplib.OK:
    print "Output from HTML request"
    
    print time.strftime('%x %X')
    print json_data['name']
    print json_data['main']['temp']

    #printText (response.read())
else:
    print "Fail to get response"
    
httpServ.close()