#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  appDHT_v1.py
#  
#  Created by MJRoBot.org 
#  10Jan18

'''
	RPi WEb Server for DHT captured data with Graph plot  
'''


from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('/home/pi/iot_ass/sensehat.db')
curs=conn.cursor()

# Retrieve LAST data from database
def getLastData():
	for row in curs.execute("SELECT * FROM SENSEHAT_data ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[0])
		temp = row[1]
		humidity = row[2]
	#conn.close()
	return time, temp, humidity


def getHistData (numSamples):
	curs.execute("SELECT * FROM SENSEHAT_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	dates = []
	temps = []
	humiditys = []
	for row in reversed(data):
		dates.append(row[0])
		temps.append(row[1])
		humiditys.append(row[2])
	return dates, temps, humiditys

def maxRowsTable():
	for row in curs.execute("select COUNT(temp) from  SENSEHAT_data"):
		maxNumberRows=row[0]
	return maxNumberRows

#initialize global variables
global numSamples
numSamples = maxRowsTable()
if (numSamples > 101):
	numSamples = 100
	
	
# main route 
@app.route("/")
def index():
	
	time, temp, humidity = getLastData()
	templateData = {
	  'time'		: time,
      'temp'		: temp,
      'humidity'			: humidity,
      'numSamples'	: numSamples
	}
	return render_template('index.html', **templateData)


@app.route('/', methods=['POST'])
def my_form_post():
    global numSamples 
    numSamples = int (request.form['numSamples'])
    numMaxSamples = maxRowsTable()
    if (numSamples > numMaxSamples):
        numSamples = (numMaxSamples-1)
    
    time, temp, humidity = getLastData()
    
    templateData = {
	  'time'		: time,
      'temp'		: temp,
      'humidity'			: humidity,
      'numSamples'	: numSamples
	}
    return render_template('index.html', **templateData)
	
	
@app.route('/plot/temp')
def plot_temp():
	times, temps, humiditys = getHistData(numSamples)
	ys = temps
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Temperature [°C]")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

@app.route('/plot/humidity')
def plot_humidity():
	times, temps, humiditys = getHistData(numSamples)
	ys = humiditys
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Humidity [%]")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=False)
