import socket
import json
from urllib2 import urlopen

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 5000

buffer_size = 4096

server_socket.bind(('', port))
server_socket.listen(10)

print("Listening on %s:%s..." % (host, str(port)))

while True:
    client_socket, address = server_socket.accept()
    data = client_socket.recv(buffer_size)

    print("Connection received from %s..." % str(address))

    msg = ""

    if host == 'tutorial-server-0':
        with open('/etc/hosts', 'r') as f:
            for line in f.readlines():
                if host not in line:
                    ip, hostname = line.split(' ')
                    r = urlopen('http://%s:5000' % hostname)
                    if r.code == 200:
                        msg += r.read() + '\n'
                    else:
                        msg += "%s is down." % hostname
        f.close()

    msg += "%s is live." % host

    client_socket.send(msg)
    client_socket.close()
