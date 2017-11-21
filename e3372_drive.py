import subprocess as sp
import serial
import time
import re

script_setup='./scripts/e3372_setup.sh'
serial_port = "/dev/ttyUSB1"
serial_baudrate = 9600
serial_readTimeOut = 10 #second

port = None
def setup():

	try:
		# setup device
		#devicePATH=/dev/ttyUSB0;
		pattern = re.compile(r'.*devicePATH=(.*);.*')	
		runState,deviceInfo = sp.getstatusoutput(script_setup)
		for deviceInfoLine in deviceInfo.split('\n'):
			match = pattern.match(deviceInfoLine)
			if match:
				print('success',match.group(1))
				serial_port = match.group(1)
				break;
		else:
			print('false')
			return False

		global port
		port = serial.Serial(serial_port,serial_baudrate)
		port.timeout  = serial_readTimeOut
	except:
		return False
	
	return True

def commandSend(command):
	port.write(command)

def commandRead():
	try:
		return port.readline()
	except:
		return None
	
	

		