#!/usr/bin/env python
import serial
import signal
import os
import boto3
import codecs
from datetime import datetime

os.makedirs('USB_Serial_Logs', exist_ok = True)

filename = datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p")
file_path = os.path.join('USB_Serial_Logs', filename + ".txt")

log_data = []
s3 = boto3.resource('s3')
BUCKET = "pylogs"

print("Press Ctrl-C To Exit The Program And Store Output To A Log File\n")

ser = serial.Serial(
        port='/dev/ttyUSB0',			# Created when you plug in a USB
        baudrate = 115200,			# Info transfer rate
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=None
)



def Keyboard_Interupt_Handler(signal, frame):	# Called on Keypress : CTRL-C
	print("\nProgram Terminated")
	if log_data:
		with codecs.open(file_path, 'w', 'ascii') as log_file:
			for item in log_data:
				log_file.write(item)
		log_file.close() 
		s3.Bucket(BUCKET).upload_file(file_path, f"{file_path}")
		print(f"Log File Saved To: {file_path}")
		print(f"Log File Saved To: Amazon S3 {BUCKET}, {filename}.txt")
	ser.close()
	exit(0)


signal.signal(signal.SIGINT, Keyboard_Interupt_Handler)  # Signal Interupt

while True:
	output = ser.readline()
	if len(output) > 2:
		output = output.decode('ascii')
		print (output, end=' ')
		log_data.append(output)

