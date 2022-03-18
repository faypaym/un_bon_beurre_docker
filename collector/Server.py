import socket
import os
from _thread import *


ServerSideSocket = socket.socket()
host = ''
port = 7777
ThreadCount = 0

ServerSideSocket.bind((host, port))
print('Socket is listening..')
ServerSideSocket.listen(5)


def multi_threaded_client(connection):
	while True:
		data = connection.recv(8192).decode("utf-8")
		ClientMultiSocket = socket.socket()
		host = '172.20.0.11'
		port = 8888
		ClientMultiSocket.connect((host, port))
		ClientMultiSocket.send(data.encode("utf-8"))
		ClientMultiSocket.close()

		#print(data)
		if not data:
			break
	connection.close()

while True:
	Client, address = ServerSideSocket.accept()
	print('Connected to: ' + address[0] + ':' + str(address[1]))
	start_new_thread(multi_threaded_client, (Client, ))
	ThreadCount += 1
	#print('Thread Number: ' + str(ThreadCount))

ServerSideSocket.close()