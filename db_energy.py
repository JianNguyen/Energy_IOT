
'''
===3 table database được sử dụng===
1. tbTY_sample_data
2. tbTY_sample_standard
3. tbTY_sample_info
'''



from database import *
import sqlite3
from mysql.connector import Error
import mysql.connector


class dbData(hostdb):
    def __init__(self):
        hostdb.__init__(self)
    def close_connect(self):
        try:
            self.conn.close()
        except:
            pass
    def query_cmd_select(self,cmd):
        try:
            self.conn = mysql.connector.connect(host=self.host,user=self.user,password=self.passwd,database=self.db)
            self.cur = self.conn.cursor()
            #excute the MySQL command
            self.cur.execute(cmd)
            #result
            self.result = eResult.Ok
            self.data_result=self.cur.fetchall()
        except Error as e:
            print(e)
            self.result = eResult.Error
        finally:
            self.close_connect()
    def query_cmd_commit(self,cmd):
        try:
            self.conn = mysql.connector.connect(host=self.host,user=self.user,password=self.passwd,database=self.db)
            self.cur = self.conn.cursor()
            #excute the MySQL command
            self.cur.execute(cmd)
            # commit your change in the database
            self.conn.commit()
            #result
            self.result = eResult.Ok
        except:
            self.result = eResult.Error
        finally:
            self.close_connect()

    def add_data(self,cabin_name,pi,group,power,date_record):
        cmd = f"insert into Energy(cabin_name,pi,group_cabin,power,date_record) values('{cabin_name}','{pi}','{group}','{power}','{date_record}')"
        #print(cmd)
        self.query_cmd_commit(cmd)

    def update_data(self,table,date,name,power,status):
        cmd = "update "+table+" set Power = "+str(power)+", Status = '"+status+"' where Date_Cal = '"+date+"' and Cabin_Name = '"+name+"'"
        #print(cmd)
        self.query_cmd_commit(cmd)

    def get_data_by_date(self,date):
        cmd = f"select * from Energy where date_record like '{date}%' order by cabin_name, date_record"
        #print(cmd)
        self.query_cmd_select(cmd)



class dbLocal():
    def close_connect(self):
        try:
            self.conn.close()
        except:
            pass

    def query_cmd_select(self,cmd):
        try:
            self.conn = sqlite3.connect('EnergyLocal.db', timeout=60)
            self.curs = self.conn.cursor()

            self.curs.execute(cmd)
            self.result = eResult.Ok
            self.data_result=self.curs.fetchall()
        except:
            self.result = eResult.Error
        finally:
            self.close_connect()
    def query_cmd_commit(self,cmd):
        try:
            self.conn = sqlite3.connect('EnergyLocal.db',timeout=60)
            self.curs = self.conn.cursor()
            
            self.curs.execute(cmd)
            
            self.conn.commit()
            self.result = eResult.Ok
        except Error as e:
            print(e)
            self.result = eResult.Error
        finally:
            self.close_connect()

    def add_data(self,power,date_record):
        cmd=f"insert into Energy_iot(power_value, date_record) values('{power}', '{date_record}');"
        self.query_cmd_commit(cmd)


    def get_all(self):
        cmd="select * from Energy_iot where status='wait';"
        self.query_cmd_select(cmd)

    def update_status(self,id):
    	cmd=f"update Energy_iot set status = 'Done' where id = {id}"
    	#print(cmd)
    	self.query_cmd_commit(cmd)





	
