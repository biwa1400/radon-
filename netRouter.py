import time
import threading
from enum import Enum

class NetRouter_Handler:
	STATES     = Enum('STATE',('DISCONNECT','READY'))
	__STATES_FSM = Enum('FSM_STATE',('DISCONNECT','RECEIVED','LISTEN'))
	

	def __init__(self,fsm_timeUnit,device_drive):
		self.state = self.STATES.DISCONNECT       # init devie state
		self.__state_fsm = self.__STATES_FSM.DISCONNECT             # init FSM_state
		self.__fsm_timeUint = fsm_timeUnit                     # set fsm time unit
		self.__device = device_drive                           # set device
		threading.Thread(target=self.threadRunning,args=()).start()
		
	def threadRunning(self):
		while True:
			if self.__state_fsm is self.__STATES_FSM.DISCONNECT:
				#change state
				self.state = self.STATES.DISCONNECT       # change FSM_state to DISCONNECT
				# setup device
				if self.__device.setup() is True:                                # device setup	
					#change state
					self.state = self.STATES.READY            # change to READY state
					self.__state_fsm = self.__STATES_FSM.LISTEN
		
			elif self.__state_fsm is self.__STATES_FSM.RECEIVED:
				pass
		
			elif self.__state_fsm is self.__STATES_FSM.LISTEN:
				readString = self.__device.commandRead()
				print(readString)
				if readString is None:
					#change state
					self.state = self.STATES.DISCONNECT       # init devie state
					self.__state_fsm = self.__STATES_FSM.DISCONNECT             # init FSM_state

		
		time.sleep(self.__fsm_timeUint)
			
	
			
		
	
	

	


	


	
		
