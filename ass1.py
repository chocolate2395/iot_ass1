#!/usr/bin/env python3
import requests
import json
import os
from datetime import datetime
import sqlite3
from sense_hat import SenseHat
dbname='/home/pi/iot_ass/sensehat.db'

# pushbullet account
ACCESS_TOKEN="o.Ldyg8nLv3qxZEhsTXphQATTH79P5XVlP"

def send_notification_via_pushbullet(title, body):
    """ Sending notification via pushbullet.
        Args:
            title (str) : title of text.
            body (str) : Body of text.
    """
    data_send = {"type": "note", "title": title, "body": body}
 
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 
                         'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something wrong')
    else:
        print('complete sending')

# namaed of cpu temp and get cup temp
def get_cpu_temp():
    res = os.popen("vcgencmd measure_temp").readline()
    t = float(res.replace("temp=","").replace("'C\n",""))
    return(t)

#named of the function
def set_temp():
    sense = SenseHat()
    time = datetime.now().strftime("%H:%M")
    humidity = sense.get_humidity()
    temp = sense.get_temperature_from_humidity()
    temp_cpu = get_cpu_temp()
#calculate the correct temperature
    temp_correct = temp - ((temp_cpu-temp)/1.5)
    logData(temp_correct, humidity)

# if temp lower then 20, it will send message via pushbullet to the user
    if temp_correct < 20:
        ip_address = os.popen('hostname -I').read()
        send_notification_via_pushbullet(ip_address, "Please bring your sweater")
# set a data into database
def logData(temp,humidity):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO SENSEHAT_data values(datetime('now', 'localtime'), (?), (?))", (temp,humidity))
    conn.commit()
    conn.close()

    displayLog(temp)
#show how many data and what date set into database.
def displayLog(temp):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    print ("\nEntire database contents:\n")
    for row in curs.execute("SELECT * FROM SenseHat_data"):
        print (row)
    conn.close()

    sense = SenseHat()
#execute the function/
def main():
    set_temp()
main()
