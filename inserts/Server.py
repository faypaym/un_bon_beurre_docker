import socket
import os
from _thread import *
from time import sleep
import mysql.connector as mariadb
import json

ServerSideSocket = socket.socket()
host = ''
port = 8888
ThreadCount = 0

ServerSideSocket.bind((host, port))
print('Socket is listening..')
ServerSideSocket.listen(5)


def insert(data):



	unit = json.loads(data)
	print(unit);

	print("tentative de co")
	connection = mariadb.connect(user='root', password='', host="172.20.0.12", port="3306", database="un_bon_beurre")
	cursor = connection.cursor()

	print("connected to database")
	sql_select_Query = "select * from units where number = %s;"


	record = (unit["unit"]["number"])
	record = (record,)
	cursor.execute(sql_select_Query, record)
	records = cursor.fetchall()

	
	print("premier select")
	#inserer seulement si unit inconu
	if cursor.rowcount == 0:

		print("UNITS INCONNU")
		mySql_insert_query = """INSERT INTO units VALUES (%s); """
		record = (unit["unit"]["number"],)
		cursor.execute(mySql_insert_query, record)
		connection.commit()

	print("--automatons---")
	print(len(unit["unit"]["automatons"]))
	for x in range(len(unit["unit"]["automatons"])):

		sql_select_Query = "select * from automatons where number = %s;"
		record = (unit["unit"]["automatons"][x]["number"],)
		print("in automatons")
		print(record)
		cursor.execute(sql_select_Query, record)
		records = cursor.fetchall()

		#creation automate
		if cursor.rowcount == 0:
			mySql_insert_query = """INSERT INTO automatons (id_unit, number, type) VALUES (%s, %s, %s); """
			record = (unit["unit"]["number"], unit["unit"]["automatons"][x]["number"], unit["unit"]["automatons"][x]["type"], )
			cursor.execute(mySql_insert_query, record)
			connection.commit()
		
		#données de production
		mySql_insert_query = """INSERT INTO productions (id_automatons, id_unit, tankTemperature, outsideTemperature, milkTemperature, milkWeight, finalizedPrdocuctWeight, ph, k, naci, salmonel, ecoli, listeria, generatedTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """
		record = (unit["unit"]["automatons"][x]["number"], unit["unit"]["number"], unit["unit"]["automatons"][x]["production"]["tankTemperature"], unit["unit"]["automatons"][x]["production"]["outsideTemperature"], unit["unit"]["automatons"][x]["production"]["milkTemperature"], unit["unit"]["automatons"][x]["production"]["milkWeight"], unit["unit"]["automatons"][x]["production"]["milkWeight"], unit["unit"]["automatons"][x]["production"]["ph"], unit["unit"]["automatons"][x]["k"], unit["unit"]["automatons"][x]["naci"], unit["unit"]["automatons"][x]["salmonel"], unit["unit"]["automatons"][x]["ecoli"], unit["unit"]["automatons"][x]["listeria"], unit["unit"]["automatons"][x]["generatedTime"],)
		cursor.execute(mySql_insert_query, record)
		connection.commit()

	connection.close()



def multi_threaded_client(connection):
	while True:
		data = connection.recv(8192).decode("utf-8")

		insert(data)

		if not data:
			break
	connection.close()

while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

ServerSideSocket.close()