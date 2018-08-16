#!/usr/bin/env python
from flask import Flask, render_template, request
app = Flask(__name__)
import sqlite3

def getData():
        conn=sqlite3.connect('/home/pi/iot_ass/sensehat.db')
        curs=conn.cursor()
        for row in curs.execute("SELECT * FROM SENSEHAT_data ORDER BY timestamp DESC LIMIT 1"):
                time = str(row[0])
                temp = row[1]
                humidity = row[2]
        conn.close()
        return time, temp, humidity
@app.route("/")
def index():
        time, temp, humidity = getData()
        templateData = {
                'time': time,
                'temp': temp,
                'humidity': humidity
        }
        return render_template('index.html', **templateData)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)

