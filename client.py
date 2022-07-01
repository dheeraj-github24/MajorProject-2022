# load additional Python modules

import base64
import io
from ipaddress import ip_address
import socket
import time
import cv2
from PIL import Image
from numpy import ndarray
import numpy as np
#import winsound


def corefn():
    camera_id = 0
    cam = cv2.VideoCapture(camera_id,cv2.CAP_DSHOW)
    count = 0
    while cam.isOpened() and count < 1:
        ret, frame1 = cam.read()
        ret2, frame2 = cam.read()
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            if cv2.contourArea(c) < 5000:
                continue
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

            if ret:
                try:
                    img = frame1[x:x+w,y:y+h]
                    cv2.imwrite('C:\\Users\\ashis\\OneDrive\\Desktop\\heroin\\base1'+str(count)+'.jpg',frame1)
                    cv2.imwrite('C:\\Users\\ashis\\OneDrive\\Desktop\\heroin2\\base2'+str(count)+'.jpg',frame2)
                    cv2.imwrite('C:\\Users\\ashis\\OneDrive\\Desktop\\hero\\crop'+str(count)+'.jpg',img)
           # frame1.paste(frame2,(x,y),mask = frame2)
            #Conv_hsv_Gray = cv2.cvtColor(difference,cv2.COLOR_BGR2GRAY)
            #ret3, mask = cv2.threshold(Conv_hsv_Gray,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

            #difference[mask != 255] = [0,0,255]

            #frame1[mask != 255] = [0,0,255]
            #frame2[mask != 255] = [0,0,255]

                    x_offset = x
                    y_offset = y
                    frame2[y_offset:y_offset+img.shape[0],x_offset:x_offset+img.shape[1]] = img
                    cv2.imwrite('C:\\Users\\ashis\\OneDrive\\Desktop\\difference\\crop'+str(count)+'.jpg',frame2)

                    count += 1
                    cv2.imshow('image',img)
                except:
                    #cv2.putText(frame1,'', (0,50), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                    print('OUT OF FRAME')
                    #winsound.PlaySound('alert.mp3', winsound.SND_ASYNC)
     
            if cv2.waitKey(10) == ord('q'):
                break
        cv2.imshow('Security Camera', frame1)
    return frame1



# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# retrieve local hostname
local_hostname = socket.gethostname()

# get fully qualified hostname
local_fqdn = socket.getfqdn()

# get the according IP address
ip_address = socket.gethostbyname(local_hostname)
#ip_address= "192.168.5.24"
# bind the socket to the port 23456, and connect
server_address = (ip_address, 1240)
sock.connect(server_address)
print ("connecting to %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))

# define example data to be sent to the server


#temperature_data = ["15", "22", "21", "26", "25", "19"]
#for entry in temperature_data:
image=corefn()
#IMAGE AA RAHA HAI BC
im_by = cv2.imencode('.jpg', image)[1].tobytes
#data_encode = np.array(im_by)
#byte_encode = data_encode.tobytes()
im = cv2.imdecode(im_by, cv2.IMREAD_COLOR)
cv2.imwrite("result.jpg", im)
#image = Image.open('/home/sdmcet/Desktop/test1.png')
#with open("C:\\Users\\ashis\\OneDrive\\Desktop\\hero\\crop3.jpg", 'rb') as image:
#f = image.read()
#b = bytearray(image)
#new_data = b[]    
sock.sendall(im)
# wait for two seconds
time.sleep(2)

sock.close()
