# Python program to be run on RPi 
# RP @ Project Team VIIT

#--------------------------------------------------------------------------------\
# TODO
# Read from record.csv for duplicate entries
# Proximity sensing
# Displaying stuff on frames

#--------------------------------------------------------------------------------
import imutils
from imutils.video import VideoStream
from pyzbar import pyzbar
import datetime
import cv2
from time import sleep

#--------------------------------------------------------------------------------
def scan_code():
	vs = VideoStream(usePiCamera=True).start()
	sleep(2)
	
	csv = open("record.csv", "w")
	found = set()
	
	success = False
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

	barcodes = pyzbar.decode(frame)
	for barcode in barcodes:
		(x, y, w, h) = barcode.rect
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type

		text = "{} ({})".format(barcodeData, barcodeType)
		cv2.putText(frame, text, (x, y - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

		if barcodeData not in found:
			csv.write(f"{datetime.datetime.now()},{barcodeData}\n")
			csv.flush()
			success = True
			found.add(barcodeData)
			
	cv2.imshow("Barcode Scanner", frame)
	
	#key = cv2.waitKey(1) & 0xFF
	#if key == ord("q"):
	#	break
	
	csv.close()
	cv2.destroyAllWindows()
	vs.stop()
	
	return success

#--------------------------------------------------------------------------------
def get_temperature():
	from smbus2 import SMBusWrapper
	address = 0x08
	sleep(2)
	
	try:
                with SMBusWrapper(1) as bus:
                        data = bus.read_i2c_block_data(address, 99, 2)
                        print('Temp {}, data {}'.format(data[0], data[1]))
       # except:
      #          print(' Oops! An error occured while measuring temperature')
      sleep(0.0005)
#--------------------------------------------------------------------------------
while True:
        proximity = 1
        if(proximity == 1):
		success = scan_code()
		if success == True:
			get_temperature()

#--------------------------------------------------------------------------------
#EOF
