from __future__ import print_function

import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time
import smbus
import time
bus = smbus.SMBus(0)
address = 0x80

# get the webcam:  
cap = cv2.VideoCapture(0)

cap.set(3,1280)
cap.set(4,1920)

time.sleep(2)

def decode(im) : 
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    # Print results
    for obj in decodedObjects:
        #print('Type : ', obj.type)
        data1=obj.data[:6].decode('utf-8')
        #print('hello',data1)
        if(data1=="emp123"):
        	print('hello',data1)
        	data = bus.read_i2c_block_data(address, 99, 2)
        	if (95<data<99):
        		print("Hi",data1,"Your temp is",data)
        	else:
        		buzzer=1
        		print("Hi",Data1,"you may not board the bus your temp is",data)


        #print('Data : ', obj.data,'\n')     
    return decodedObjects


font = cv2.FONT_HERSHEY_SIMPLEX

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         
    decodedObjects = decode(im)

    for decodedObject in decodedObjects: 
        points = decodedObject.polygon
     
        # If the points do not form a quad, find convex hull
        if len(points) > 4 : 
          hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
          hull = list(map(tuple, np.squeeze(hull)))
        else : 
          hull = points;
         
        # Number of points in the convex hull
        n = len(hull)     
        # Draw the convext hull
        for j in range(0,n):
          cv2.line(frame, hull[j], hull[ (j+1) % n], (255,0,0), 3)

        x = decodedObject.rect.left
        y = decodedObject.rect.top

        #print(x, y)

        #print('Type : ', decodedObject.type)
        #print('Data : ', decodedObject.data,'\n')

        barCode = str(decodedObject.data)
        
        





        #cv2.putText(frame, barCode, (x, y), font, 1, (0,255,255), 2, cv2.LINE_AA)
               
    # Display the resulting frame
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break   

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()