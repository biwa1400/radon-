import serial

serial_baudrate = 9600
serial_readTimeOut = 2 #second

port = None
def setup():	
	# setup serial
	global port
	port = serial.Serial(serial_port,serial_baudrate)
	port.timeout  = serial_readTimeOut
	#port.open()


def commandSend(command):
	port.write(command)

def commandRead():
	return port.readline()
	
setup()
while True:
	print(commandRead())

	

		