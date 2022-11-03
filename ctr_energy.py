from db_energy import *




class ctr_energy():
    def __init__(self):
        self.dbServer = dbData()
        self.dbLocal= dbLocal()
        

    # def update_data_server(self,table,date,name,power,status):
    #     self.dbServer.get_data_by_date(table,date,name)
    #     if self.dbServer.result==eResult.Ok:
    #         if len(self.dbServer.cur.fetchall())>0:
    #             self.dbServer.update_data(table,date,name,power,status)
    #             print("Updated")
    #         else:
    #             self.dbServer.add_data(table,date,name,power,status)
    #             print("Inserted")
    #         return True
    #     return False
    # def check_data_sent_server(self,table,date,name):
    #     self.dbServer.get_data_by_date(table,date,name)
    #     if self.dbServer.result==eResult.Ok:
    #         if len(self.dbServer.cur.fetchall())>0:
    #             return True
    #     return False

    def update_data_server(self,cabin_name,pi,group,power,date_record):
        self.dbServer.add_data(cabin_name,pi,group,power,date_record)
        if self.dbServer.result==eResult.Ok:
            return True
        return False

    def get_data_server(self,date):
        self.dbServer.get_data_by_date(date)
        if self.dbServer.result==eResult.Ok:
            return self.dbServer.data_result
        return None

    # def save_data_local(self):
    #     self.dbLocal.get_data_by_date(table,date,name)
    #     if self.dbLocal.result==eResult.Ok:
    #         if len(self.dbLocal.cur.fetchall())>0:
    #             self.dbLocal.update_data(table,date,name,power,status)
    #             print("Updated")
    #         else:
    #             self.dbLocal.add_data(table,date,name,power,status)
    #             print("Inserted")
    #         return True
    #     return False

    def save_data_local(self, power, date_record):
        self.dbLocal.add_data(power, date_record)
        if self.dbLocal.result==eResult.Ok:
            return True
        return False

    def update_status_local(self,id):
        self.dbLocal.update_status(id)
        if self.dbLocal.result==eResult.Ok:
            return True
        return False

    def get_data_local(self):
        self.dbLocal.get_all()
        if self.dbLocal.result==eResult.Ok:
            return self.dbLocal.data_result
        return None



    

