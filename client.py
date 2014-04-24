import socket
import sys

BUFFSIZE = 4096

if len(sys.argv) != 3 :
	print "usage: python %s <hostname> <outfile>" % sys.argv[0]
	sys.exit(1)

for res in socket.getaddrinfo(sys.argv[1], 3490, socket.AF_INET, socket.SOCK_STREAM):
	family, socktype, proto, canonname, sockaddr = res
	try:
		s = socket.socket(family, socktype, proto)
	except socket.error as msg:
		s = None
		continue
	try:
		s.connect(sockaddr)
	except socket.error as msg:
		s.close()
		s = None
		continue
if s is None:
	print "Could not connect to %s" % sys.argv[1]
	sys.exit(1)

outfile = open(sys.argv[2], "w")

data = s.recv(BUFFSIZE)
while data :
	outfile.write(data)
	data = s.recv(BUFFSIZE)

outfile.close()
s.close()
s = None