import socket
import sys

BUFFSIZE = 4096

if len(sys.argv) != 3 :
	print "usage: python %s <hostname> <outfile>" % sys.argv[0]
	sys.exit(1)

for res in socket.getaddrinfo(sys.argv[1], 3490, socket.AF_UNSPEC, socket.SOCK_STREAM):
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
	break;
if s is None:
	print "Could not connect to %s" % sys.argv[1]
	sys.exit(1)

# open the file to write what the server sends us
outfile = open(sys.argv[2], "r+")
# open a file to store the progress of the transfer
pastSession = open("clientlog", "a+")
pastSession.seek(0) # go to the begining of this file

# if the past transfer was working on the same file, tell the server to start from an offset
if pastSession.readline() == sys.argv[2] : 
	offset = int(pastSession.readline())
	s.sendall(str(offset))
	outfile.seek(offset * BUFFSIZE)
# otherwise, have the server start at the beginning
else :
	s.sendall("0")

# clear the log file
pastSession.seek(0)
pastSession.truncate()
# write to the log file the title and size so far
pastSession.write(sys.argv[2] + "\n")
pastSession.write("0")
i = 0
data = s.recv(BUFFSIZE)
while data :
	outfile.write(data)
	i += 1
	# clear the log file
	pastSession.seek(0)
	pastSession.truncate()
	# write to the log file the title and size so far
	pastSession.write(sys.argv[2] + "\n")
	pastSession.write(str(i) + "\n")
	data = s.recv(BUFFSIZE)

# this file transfer finished, clear the log file
pastSession.seek(0)
pastSession.truncate()
pastSession.close()

outfile.close()
s.close()
s = None