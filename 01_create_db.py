import sqlite3 as lite 
import sys 
connection = lite.connect('sensehat.db') 
with connection: 
    cur = connection.cursor() 
    cur.execute("DROP TABLE IF EXISTS SENSEHAT_data") 
    cur.execute("CREATE TABLE SENSEHAT_data(timestamp DATETIME, temp NUMERIC, humidity NUMERIC)")
