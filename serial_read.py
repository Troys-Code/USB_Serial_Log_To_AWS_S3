#!/usr/bin/env python
import time
import serial
import signal

print("Press Ctrl-C To Exit Program")

ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

def Keyboard_Interupt_Handler(signal, frame):
	print("\nProgram Terminated")
	ser.close()
	exit(0)

signal.signal(signal.SIGINT, Keyboard_Interupt_Handler)

while True:
	output = ser.readline()
	if (output):
		if (b'BLDC response Timed out' in output): # byte type introduced in python 3
			continue
		else:
			print (output.decode('utf-8'), end=' ')
