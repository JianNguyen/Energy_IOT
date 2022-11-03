import sqlite3
from mysql.connector import Error
import datetime
from db_energy import *
'''
try:
    conn = sqlite3.connect('/home/pi/Desktop/Energy_IOT/EnergyLocal.db')
    curs = conn.cursor()
    timenow = datetime.datetime.now()
    ymd = timenow.strftime("%Y") + "-" + timenow.strftime("%m") + "-" + timenow.strftime("%d")
    hm  = timenow.strftime("%H") + ":" + timenow.strftime("%M")
    m   = timenow.strftime("%M")
    time_to_update = ymd + " " + timenow.strftime("%H")
    cmd="INSERT INTO Energy (Date_Time, Power, Flag) VALUES ('"+str(time_to_update)+"', 10, 'Inserted');"
    #cmd="INSERT INTO Energy (Power, Flag) VALUES (20, 'Inserted');"
    print(cmd)
    curs.execute(cmd)
    conn.commit()        
    print('local ok')   
except Error as e:
        print(e)
'''
timenow = datetime.datetime.now()
ymd = timenow.strftime("%Y") + "-" + timenow.strftime("%m") + "-" + timenow.strftime("%d")
hm  = timenow.strftime("%H") + ":" + timenow.strftime("%M")
m   = timenow.strftime("%M")
time_to_update = ymd + " " + timenow.strftime("%H")
db_local=dbLocal()
db_local.get_data('Inserted')
if db_local.result == eResult.Ok:
    dt = db_local.curs.fetchall()
    print(dt)