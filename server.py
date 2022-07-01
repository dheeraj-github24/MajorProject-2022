import base64
import socket

from PIL import Image
import io

import cv2



#ZZimport byte_array import byte_data

# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# retrieve local hostname
local_hostname = socket.gethostname()

# get fully qualified hostname
local_fqdn = socket.getfqdn()

# get the according IP address
ip_address = socket.gethostbyname(local_hostname)

# output hostname, domain name and IP address
print ("working on %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))

# bind the socket to the port 23456
server_address = (ip_address, 1240)
print ('starting up on %s port %s' % server_address)
sock.bind(server_address)

# listen for incoming connections (server mode) with one connection at a time
sock.listen(1)

while True:
    # wait for a connection
    print ('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        # show who connected to us
        print ('connection from', client_address)

        # receive the data in small chunks and print it
        while True:
            data = connection.recv(102400)
            #print(data)
            if data:
                #BASE1= base64.b64decode(data)
                im = cv2.imdecode(data, cv2.IMREAD_COLOR)
                cv2.imwrite("result.jpg", im)
                
                #print(BASE1)      
                #stream=io.BytesIO(data.decode())
                #img=Image.open(stream).convert("RGBA")
                #stream.close()

                #img.save('C:\\Users\\ashis\\OneDrive\\Desktop\\gotit1.jpg')
            else:
                # no more data -- quit the loop
                print ("no more data.")
                break
    finally:
        # Clean up the connection
        connection.close()
