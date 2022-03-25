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

	connection = mariadb.connect(user='root', password='', host="172.20.0.12", port="3306", database="un_bon_beurre")
	cursor = connection.cursor()

	print("connected to database")
	sql_select_Query = "select * from units where number = %s;"


	record = (unit["unit"]["number"])
	record = (record,)
	cursor.execute(sql_select_Query, record)
	records = cursor.fetchall()

	
	#inserer seulement si unit inconu
	if cursor.rowcount == 0:

		print("UNITS INCONNU")
		mySql_insert_query = """INSERT INTO units VALUES (%s); """
		record = (unit["unit"]["number"],)
		cursor.execute(mySql_insert_query, record)
		connection.commit()

	print("--automatons---")


	for x in range(len(unit["unit"]["automatons"]) -1):
		
		print("boucle")
		print(x)

		sql_select_Query = "select * from automatons where number = %s;"
		record = (unit["unit"]["automatons"][x]["number"],)
		cursor.execute(sql_select_Query, record)
		records = cursor.fetchall()

		id_automaton = -1
		for row in records:
			id_automaton = row[0]

		#creation automate
		if cursor.rowcount == 0:
			mySql_insert_query = """INSERT INTO automatons (id_unit, number, type) VALUES (%s, %s, %s); """
			record = (unit["unit"]["number"], unit["unit"]["automatons"][x]["number"], unit["unit"]["automatons"][x]["type"], )
			print("avant exec")
			print(record)
			cursor.execute(mySql_insert_query, record)
			connection.commit()
		

		print("insertion production")

		#données de production
		mySql_insert_query = """INSERT INTO productions (id_automaton, id_unit, tankTemperature, outsideTemperature, milkWeight, finalizedProductWeight, ph, k, naci, salmonel, ecoli, listeria, generatedTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """
		record = (id_automaton, unit["unit"]["number"], unit["unit"]["automatons"][x]["production"]["tankTemperature"], unit["unit"]["automatons"][x]["production"]["outsideTemperature"], unit["unit"]["automatons"][x]["production"]["milkWeight"], 2, unit["unit"]["automatons"][x]["production"]["ph"], unit["unit"]["automatons"][x]["production"]["k"], unit["unit"]["automatons"][x]["production"]["naci"], unit["unit"]["automatons"][x]["production"]["salmonel"], unit["unit"]["automatons"][x]["production"]["ecoli"], unit["unit"]["automatons"][x]["production"]["listeria"], unit["unit"]["automatons"][x]["production"]["generatedTime"],)
		
		print("record:")
		print(record)

		
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