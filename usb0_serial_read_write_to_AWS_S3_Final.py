#!/usr/bin/env python
import serial
import signal
import os
import boto3
from datetime import datetime


def Keyboard_Interupt_Handler(signal, frame):	# Called on Keypress : CTRL-C
	""" 

	Description:
	____________
	- Occurs on keypress CTRL-C which handles the exit program procedure
	- Writes log to the directory created in main and to Amazon S3 Bucket

	"""

	print("\nProgram Terminated")
	if log_data:
		log_file = open(file_path, "w")
		for item in log_data:
			log_file.write(item)
		log_file.close() 
		s3.Bucket(BUCKET).upload_file(file_path, f"{file_path}")
		print(f"Log File Saved To: {file_path}")
		print(f"Log File Saved To: Amazon S3 {BUCKET}, {file_name}.txt")
	ser.close()
	exit(0)


def main():
	"""

	Description:
	____________
	- Creates directory 'USB_Serial_Logs' to store the serial output
	- Reads from serial via USB-0 
	- Displays serial output to console
	- CTRL-C Exits the program and stores output to a log file.

	Usage:
	______
	- Plug in serial USB cable before running the script
	- Ensure that only a single USB is connected
	- Once the script is running serial data will be displayed to console
	- To exit the program and store the results Press CTRL-C
	- Results stored in directory 'USB_Serial_Logs' and to Amazon S3 Bucket

	Setup:
	______
	- Prerequisite: Must have python and pip installed
	- Install AWS CLI using command in terminal - sudo pip install awscli
	- Configure AWS Credentials using command in terminal -  aws configure

	"""

	global file_name, file_path, log_data, s3, BUCKET, ser
	file_name = datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p")
	file_path = os.path.join('USB_Serial_Logs', file_name + ".txt")
	log_data = []
	s3 = boto3.resource('s3')
	BUCKET = "pylogs"

	ser = serial.Serial(
        	port='/dev/ttyUSB0',		# Created when you plug in a USB
        	baudrate = 115200,		# Info transfer rate
        	parity = serial.PARITY_NONE,
        	stopbits = serial.STOPBITS_ONE,
        	bytesize = serial.EIGHTBITS,
        	timeout = None
	)

	os.makedirs('USB_Serial_Logs', exist_ok = True)

	signal.signal(signal.SIGINT, Keyboard_Interupt_Handler)

	print("Press Ctrl-C To Exit And Store Log File\n")

	while True:
		output = ser.readline()
		if len(output) > 2:
			output = output.decode('utf-8')
			log_data.append(output)  # Append to list
			print (output, end=' ')  # Print to console


if __name__ == "__main__":
	main()
