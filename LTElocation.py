import threading
import time
from enum import Enum
import re
import requests
from json import dumps


class Location:
	
	states_FSM=Enum('states_FSM',('disconnected','updating','sleep'))
	
	def __init__(self,netRouter,updateTime,mcc,mnc):
		self.router = netRouter
		self.updateTime = updateTime
		self.state_FSM = Location.states_FSM.disconnected
		self.mcc = mcc
		self.mnc = mnc
		self.lac = 0
		self.cid = 0
		threading.Thread(target=self.updateFSM,args=()).start()
	
	
	
	def updateFSM(self):
		while True:
			if self.state_FSM is Location.states_FSM.disconnected:
				if self.router.state_device is not self.router.states_device.disconnected:
					self.state_FSM = Location.states_FSM.updating
				else:
					time.sleep(self.router.hangupTime)
			
			elif self.state_FSM is Location.states_FSM.updating:
				if self.router.state_device is self.router.states_device.free:
					self.router.request('AT+CREG?\r\n')
					
					while self.router.state_device is not self.router.states_device.response:
						time.sleep(self.router.commandResponseTime)
						if self.router.state_device is not  self.router.states_device.busy:
							break
					if self.router.state_device is self.router.states_device.response:
						print ('response')
						for i in self.router.getResponse():
							print(i.title)
							if i.title == "+CREG":
								print(i.content)
								
								pattern = re.compile(r'.*\"(.*)\",\"(.*)\".*')
								match = pattern.match(i.content)
								if match:
									try:
										self.lac = int(match.group(1),16)
										self.cid = int(match.group(2),16)
									except:
										print("cannot convert from char to hex")
								else:
									print("not match!")
					self.state_FSM = Location.states_FSM.sleep

			elif self.state_FSM is Location.states_FSM.sleep:
				time.sleep(self.updateTime)
				self.state_FSM = Location.states_FSM.updating
			
