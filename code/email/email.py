#!/usr/bin/python

## This script, when executed, sends an email message from your Pi 
## to a specified recipient with a brief message.

## First you must set up 2-step verication with google accounts. Then get an App-specific password  
## that you can use with your Pi. (See Video). This password is used in the script below.

import smtplib
import mimetypes
import email
import email.mime.application
import sys
from time import strftime

me='myEmail@gmail.com'  #####Sender's email####
you='yourEmail@newpaltz.edu'     ### Receiver's email########
another='anotherPerson@gmail.com'   ### Another recipient ####
msg = email.mime.Multipart.MIMEMultipart()
msg['Subject'] = 'Test from Pi'
msg['From'] = me
msg['To'] = you
body=email.mime.Text.MIMEText("This is a test from my Pi-----"+strftime("%Y-%m-%d %H:%M:%S"))
msg.attach(body)
s = smtplib.SMTP('smtp.gmail.com:587')
s.starttls()
s.login(me,'bubw ukby aaip aext') ## Use your App-specific password from google##########
s.sendmail(me,[you,another],msg.as_string())
s.quit()

###References
#https://docs.python.org/2/library/email-examples.html
###http://solvingmytechworld.blogspot.com/2013/01/send-email-through-gmail-running-script.html
### http://stackoverflow.com/questions/1966073/how-do-i-send-attachments-using-smtp/8243031#8243031
