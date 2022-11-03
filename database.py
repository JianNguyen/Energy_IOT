'''
Định nghĩa connect to local database server
'''

import mysql.connector
from enum import Enum, IntEnum
import sqlite3
from mysql.connector import Error
class eResult(IntEnum):
	Unknown=0
	Ok=1
	Error=2
	
class hostdb():
	def __init__(self):
		# ~ self.host_local = "localhost"
		self.host = "ifsmvp.com"
		self.user = "ifsmvp"
		self.passwd = "tech@marueivn.com"
		self.db = "ifsmvp_energy_database"



