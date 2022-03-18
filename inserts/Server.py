import socket
import os
from _thread import *
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


	print("tentative de co")
	connection = mariadb.connect(user='root', password='', host="172.20.0.12", port="3306", database="un_bon_beurre")
	cursor = connection.cursor()

	print("connected")
	sql_select_Query = "select * from units where number = %s;"
	record = (unit["unit"]["number"])
	cursor.execute(sql_select_Query, record)
	records = cursor.fetchall()
	
	print("premier select")
	#inserer seulement si unit inconu
	if cursor.rowcount == 0:
		mySql_insert_query = """INSERT INTO units VALUES (%s); """
		record = (unit["unit"]["number"])
		cursor.execute(mySql_insert_query, record)
		connection.commit()



	for x in range(len(unit["unit"]["automaton"])):

		sql_select_Query = "select * from automatons where number = %s;"
		record = (unit["unit"]["automaton"][x]["number"])
		cursor.execute(sql_select_Query, record)
		records = cursor.fetchall()

		#creation automate
		if cursor.rowcount == 0:
			mySql_insert_query = """INSERT INTO automatons (id_unit, number, type) VALUES (%s, %s, %s); """
			record = (unit["unit"]["number"], unit["unit"]["automaton"][x]["number"], unit["unit"]["automaton"][x]["type"] )
			cursor.execute(mySql_insert_query, record)
			connection.commit()
		
		#données de production
		mySql_insert_query = """INSERT INTO productions (id_automaton, id_unit, tankTemperature, outsideTemperature, milkTemperature, milkWeight, finalizedPrdocuctWeight, ph, k, naci, salmonel, ecoli, listeria, generatedTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """
		record = (unit["unit"]["automaton"][x]["number"], unit["unit"]["number"], unit["unit"]["automaton"][x]["production"]["tankTemperature"], unit["unit"]["automaton"][x]["production"]["outsideTemperature"], unit["unit"]["automaton"][x]["production"]["milkTemperature"], unit["unit"]["automaton"][x]["production"]["milkWeight"], unit["unit"]["automaton"][x]["production"]["milkWeight"], unit["unit"]["automaton"][x]["production"]["ph"], unit["unit"]["automaton"][x]["k"], unit["unit"]["automaton"][x]["naci"], unit["unit"]["automaton"][x]["salmonel"], unit["unit"]["automaton"][x]["ecoli"], unit["unit"]["automaton"][x]["listeria"], unit["unit"]["automaton"][x]["generatedTime"])
		cursor.execute(mySql_insert_query, record)
		connection.commit()

	connection.close()



def multi_threaded_client(connection):
	while True:
		data = connection.recv(8192).decode("utf-8")
		print(data)
		
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