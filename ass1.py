#!/usr/bin/env python3
import requests
import json
import os
from datetime import datetime
from sense_hat import SenseHat

ACCESS_TOKEN="o.9rpjP4gKMOcHyJhURQVMswfjq37U5WKl"

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

# namaed of cpu temp
def get_cpu_temp():
    res = os.popen("vcgencmd measure_temp").readline()
    t = float(res.replace("temp=","").replace("'C\n",""))
    return(t)

sense = SenseHat()
time = datetime.now().strftime("%H:%M")
humidity = sense.get_humidity()
temp = sense.get_temperature_from_humidity()
temp_cpu = get_cpu_temp()
#calculate the correct temperature
temp_correct = temp - ((temp_cpu-temp)/1.5)
#main function
if temp_correct > 20:
    ip_address = os.popen('hostname -I').read()
    send_notification_via_pushbullet(ip_address, "Please bring your sweater")

#Execute
