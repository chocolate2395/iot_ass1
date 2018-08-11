import os
from sense_hat import SenseHat
import time
import requests
import json
 
ACCESS_TOKEN="o.ttZEWeo4DjElL6en6e9aBgY0dABbyxjK"

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

def get_cpu_temp():
  res = os.popen("vcgencmd measure_temp").readline()
  t = float(res.replace("temp=","").replace("'C\n",""))
  return(t)


sense = SenseHat()

while True:
  t = sense.get_temperature_from_humidity()
  t_cpu = get_cpu_temp()
  h = sense.get_humidity()
  p = sense.get_pressure()

  # calculates the real temperature compesating CPU heating
  t_corr = t - ((t_cpu-t)/1.5)
  
  print("t=%.1f  t_cpu=%.1f  t_corr=%.1f  h=%d  p=%d" % (t, t_cpu, t_corr, round(h), round(p)))
  
  time.sleep(5)
  if t_corr < 20:
        ip_address = os.popen('hostname -I').read()
        send_notification_via_pushbullet(ip_address, "Please bring your sweater!")

