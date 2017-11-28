import subprocess as sp
import serial
import time
import re


script_setup='./scripts/e3372_setup.sh'
serial_port = "/dev/ttyUSB1"
serial_baudrate = 9600
commandResponseTime = 0.02 #s
max_commandResponseTime = 5 #s

port = None
def setup():

	try:
		# setup device
		pattern = re.compile(r'.*devicePATH=(.*);.*')	
		runState,deviceInfo = sp.getstatusoutput(script_setup)
		for deviceInfoLine in reversed(deviceInfo.split('\n')):
			match = pattern.match(deviceInfoLine)
			if match:
				serial_port = match.group(1)
				break;
		else:
			print(deviceInfoLine)
			return False

		global port
		port = serial.Serial(serial_port,serial_baudrate)
	except:
		return False
	
	return True

def commandSend(command):
	try:
		port.write(command)
	except:
		return False
	
	return True
		

def commandRead():
	try:
		return port.readline()
	except:
		return None
		
def ckeck_fix_disconnect():
	runState,deviceInfo = sp.getstatusoutput('ifconfig eth1')
	if runState is 0:
		sp.getstatusoutput('ifconfig eth1 up')
		sp.getstatusoutput('udhcpc -BFs -i eth1')
		sp.getstatusoutput('route add default gw 192.168.8.1')

class Packet:
	def __new__(cls,packetString):
		#print('string: ',packetString)
		pattern = re.compile(r'(.*):(.*)$')
		match = pattern.match(packetString)
		if match:
			object = super().__new__(cls)
			object.title = match.group(1)
			object.content = match.group(2)
			#print("match command: ",object.content)
			return object
		else:
			return None
	

			
			
	
	
	

		