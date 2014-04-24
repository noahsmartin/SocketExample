import socket
import sys

BUFFSIZE = 4096

if len(sys.argv) != 2 :
	print "usage: python %s <filename>" % sys.argv[0]
	sys.exit(1)

for res in socket.getaddrinfo(None, 3490, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
	family, socktype, proto, canonname, sockaddr = res
	try:
		s = socket.socket(family, socktype, proto)
	except socket.error as msg:
		s = None
		continue
	try:
		s.bind(sockaddr)
		s.listen(0)
	except socket.error as msg:
		s.close()
		s = None
		continue
	break;
if s is None:
	print "Server failed to bind"
	sys.exit(1)

file = open(sys.argv[1], "r")

con, addr = s.accept()
print "Connected to ", addr

data = file.read(BUFFSIZE)
while data :
	con.sendall(data)
	data = file.read(BUFFSIZE)

con.close()
s.close()
file.close()

