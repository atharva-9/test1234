import adafruit_mlx90614
import RPi.GPIO as GPIO
import time
from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time

dummy = emp123
#cam setup
cap = cv2.VideoCapture(0)
#image dimension
cap.set(2,560)
cap.set(1,960)

GPIO.setmode(GPIO.BOARD)

TRIG = 16
ECHO = 18
i=0
#i2c setup
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
#MLX Sensor 
i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
mlx = adafruit_mlx90614.MLX90614(i2c)

def decode(im) : 
    # read qr code
    decodedObjects = pyzbar.decode(im)
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data,'\n')     
    return decodedObjects

def qr():
	while(cap.isOpened()):
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
         
        # detect the position blocks
        n = len(hull)     
        for j in range(0,n):
          cv2.line(frame, hull[j], hull[ (j+1) % n], (255,0,0), 3)

        x = decodedObject.rect.left
        y = decodedObject.rect.top

        print(x, y)

        print('Type : ', decodedObject.type)
        print('Data : ', decodedObject.data,'\n')

        barCode = str(decodedObject.data)
        
               
    # Display the resulting frame
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('s'): # wait for 's' key to save 
        cv2.imwrite('Capture.png', frame)     


try:
    while True:
       GPIO.output(TRIG, True)
       time.sleep(0.00001)
       GPIO.output(TRIG, False)

       while GPIO.input(ECHO)==0:
          pulse_start = time.time()

       while GPIO.input(ECHO)==1:
          pulse_end = time.time()

       pulse_duration = pulse_end - pulse_start

       distance = pulse_duration * 17150

       distance = round(distance+1.15, 2)
  
       if distance<=50 and distance>=5:
          print ("Scan the QR CODE")
          qr()
          if(barCode=dummy)

          print("Object Temp: ", mlx.object_temperature)# temperature results in celsius

          i=1
          
       if distance>50 and i==1:
          print ("Come Closer..")
          i=0
       time.sleep(2)


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()






