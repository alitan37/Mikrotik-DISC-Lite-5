import socket 

TCP_PORT1 = 3737
BUFFER_SIZE = 20

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', TCP_PORT1))
s.listen(1)

conn, addr = s.accept()
print "Connection address:", addr
while True:
   data = conn.recv(BUFFER_SIZE)
   if not data: break
   print data
   conn.send(data) #echo
conn.close()
