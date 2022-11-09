import os
import time
import serial
import urllib
from urllib.request import urlopen
from mysql.connector import Error
import mysql.connector
import datetime
import binascii
import sqlite3
from subprocess import call
import sys
from ctr_energy import *
import subprocess
from gpiozero import CPUTemperature
import socket
from threading import Thread,Lock
from getmac import get_mac_address as gma
import psutil


ser = serial.Serial(
    port     = '/dev/ttyUSB0',
    baudrate = 19200,
    stopbits = serial.STOPBITS_ONE,
    parity   = serial.PARITY_EVEN,
    bytesize = serial.EIGHTBITS,
    timeout  = 0
    )



def readdata():
    #print('reading')
    flag=0
    command = b'\x01\x03\x05\x80\x00\x02\xC5\x2F'
    ser.write(command)
    ser.flush()
    time.sleep(1)
    s = ser.readline()
    try:
        while len(s)<9 and len(s)>2:
            if s[len(s)-1]==10:
                p=ser.readline()
                print(p)
                s=s+p
    except:
        print("Time out")
            
    #s = b'\x01\x03\x04\x00\x54\x02\x3F\xfa\x93'
    #s = b'\x01\x03\x04\x00\x3F\xfa\x93'
    time.sleep(1)
    a = binascii.hexlify(s)
    print(s)
    #print(len(s))
    print(a)
    #print(a[0:4])
    if((len(s)==9) & (a[0:4] == b'0103')):
       # print(s) 
       # print(len(s))
        power=int(a[6:14],16)
        print("Read data successfully")
        print(power)
        
        flag = 1
    else:
        print("Read data fail")
        flag = 0
        power = 0
    return power,flag




def ping_to_check_connect(address):
    timeout = 2
    ping_result = False
    res=call(['ping',address,'-w',str(timeout)])
    if res==0:
        print('ping to ',address, ' OK!', ' res: ',res)
        ping_result=True
    elif res==2:
        print('no respond from ',address, ' res: ',res)
    else:
        print('ping to ',address, ' Failed!', ' res: ',res)

    return ping_result

def sync_time_from_ntpserver(ntpserver_address):
    res=call(['sudo','ntpdate','-u',ntpserver_address])
    return res

def save_data_to_local(db,lock):
    flag_read_data=True
    while True:
        try:
            nowtime=datetime.datetime.now()
            #if int(nowtime.strftime("%M"))<10 and flag_read_data:
            if (int(nowtime.strftime("%M"))<10 or (int(nowtime.strftime("%M"))>=30 and int(nowtime.strftime("%M"))<40)) and flag_read_data:
                print("---------------------------------------")
                print(nowtime)
                power,flag=readdata()
                if flag==1:
                    lock.acquire()
                    rs_save=db.save_data_local(power, str(nowtime))
                    if rs_save:
                        print("Save local ok")
                        flag_read_data=False
                    else:
                        print("Save local fail")
                    lock.release()
                    print("---------------------------------------")
                else:
                    time.sleep(5)
            #elif int(nowtime.strftime("%M"))>=10:
            elif not (int(nowtime.strftime("%M"))<10 or (int(nowtime.strftime("%M"))>=30 and int(nowtime.strftime("%M"))<40)):
                flag_read_data=True
            time.sleep(10)
        except Exception as e:
            print("Can't save data to local: ", e)

def save_data_to_server(db,cabin_name,pi,group,lock):

    while True:
        try:
            #Read data from local with status wait
            print("------------------------------------------")
            nowtime=datetime.datetime.now()
            print(nowtime)
            print("Upload data to server")
            lock.acquire()
            rs_data_local=db.get_data_local()
            lock.release()
            if rs_data_local !=None:
                if len(rs_data_local)>0:
                    #Update data to server
                    for i in range(len(rs_data_local)):
                        rs_update=db.update_data_server(cabin_name,pi,group,rs_data_local[i][1],rs_data_local[i][2])
                        if rs_update:
                            lock.acquire()
                            rs_status=db.update_status_local(str(rs_data_local[i][0]))
                            lock.release()

                            print("Update to server ok")
                        else:
                            print("Update to server fail")
                else:
                    print("No data to upload")
            print("-----------------------------------------------")
            time.sleep(60)
        except Exception as e:
            print("Can't put data to server: ",e)



def read_temperature():
    #Đọc nhiệt độ
    cpu=CPUTemperature()
    temp=str(round(float(cpu.temperature),1))

    #Đọc CPU
    CPU=str(psutil.cpu_percent())
        
    #Đọc RAM
    cmd = "free -m | awk 'NR==2{printf \"%.2f\",$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True ).decode().strip()

    #Đọc ROM
    cmd = "df -h | awk '$NF==\"/\"{printf \"%.2f\", $3*100/$2}'"
    Disk = subprocess.check_output(cmd, shell = True ).decode().strip()

    return temp, CPU, MemUsage, Disk

def check_system(cabin,db):
    flag_send=True
    while True:
        try:
            temp, cpu, ram, rom = read_temperature()
            if (float(temp)>80 or float(cpu)>90 or float(ram)>90 or float(rom)>80) and flag_send:
                #Send to server
                print("----------------------------------------")
                print(temp, cpu, ram, rom)
                rs_update=db.add_parameter_pi(cabin, temp, cpu, ram, rom)
                if rs_update:
                    print("Send alert to server ok")
                    flag_send=False
                else:
                    print("Send alert to server fail")
                print("----------------------------------------")
            elif not (float(temp)>80 or float(cpu)>90 or float(ram)>90 or float(rom)>80):
                flag_send=True
                time.sleep(10)
        except Exception as e:
            print("Can't read parameter pi: ", e)

def read_ip():
    #Đọc IP trên pi
    cmd = "hostname -I"
    IP = subprocess.check_output(cmd, shell = True ).decode().strip()
    
    #Đọc IP trên window
    #IP=socket.gethostbyname(socket.gethostname())
    return IP


if __name__=='__main__':
    cabin_name='53'
    ip=read_ip()+' - '+gma()
    group="Offices"
    db=ctr_energy()
    lock=Lock()
    thr=Thread(target=save_data_to_server, args=(db,cabin_name,ip,group,lock))
    thr.start()
    thr_temp=Thread(target=check_system, args=(cabin_name,db))
    thr_temp.start()
    save_data_to_local(db,lock)



    
