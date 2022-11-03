from ctr_energy import *
import datetime
timenow = datetime.datetime.now()
ymd = timenow.strftime("%Y") + "-" + timenow.strftime("%m") + "-" + timenow.strftime("%d")
hm  = timenow.strftime("%H") + ":" + timenow.strftime("%M")
m   = timenow.strftime("%M")
time_to_update = ymd + " " + timenow.strftime("%H")
db= ctr_energy()

print(db.update_data('NC',time_to_update,'2',int(m),'Ok'))