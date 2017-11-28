import time
import threading
from enum import Enum

class NetRouter_Handler:
	states_FSM_receive=Enum('states_FSM_receive',('disconnected','listening','received','processing'))
	states_FSM_request=Enum('states_FSM_request',('disconnected','sending','waiting_receive','receving','waiting_read','destroy'))
	states_device=Enum('states_device',('free','busy','response','disconnected'))
	
	def __init__(self,hangupTime,waitReadTime,device_drive):
		#init parameters
		self.hangupTime = hangupTime
		self.waitReadTime = waitReadTime
		self.device = device_drive
		self.totalCommandResponseTime = 0
		self.commandResponseTime = self.device.commandResponseTime
		self.response = []
		
		# init state
		self.state_FSM_receive = NetRouter_Handler.states_FSM_receive.disconnected #init state_FSM_receive to disconnected
		self.state_FSM_request = NetRouter_Handler.states_FSM_request.disconnected #init state_FSM_request to disconnected
		self.state_device = NetRouter_Handler.states_device.disconnected #init state_device to disconnected

		# start receive_FSM
		threading.Thread(target=self.receiveFSM,args=()).start()
		threading.Thread(target=self.keepConnect,args=()).start()
	
	def keepConnect(self):
		while True:
			print('check reconnect!!!!!!!!!!!!!')
			self.device.ckeck_fix_disconnect()
			time.sleep(120)
	
	#interface
	def request(self,requestString):
		if self.state_FSM_request is NetRouter_Handler.states_FSM_request.destroy:
			self.state_FSM_request = NetRouter_Handler.states_FSM_request.sending
			threading.Thread(target=self.requestFSM,args=(requestString,)).start()
			return True
		else:
			return False
		
	
	#interface
	def getResponse(self):
		if self.state_device is NetRouter_Handler.states_device.response:
			self.state_device = NetRouter_Handler.states_device.free
			response = self.response
			if self.state_FSM_request is NetRouter_Handler.states_FSM_request.waiting_read:
				self.state_FSM_request = NetRouter_Handler.states_FSM_request.destroy
				
			return response
		else:
			return None
	
	def requestFSM(self,requestString):
		while True:
			if self.state_FSM_request is NetRouter_Handler.states_FSM_request.disconnected:
				time.sleep(self.hangupTime)
			
			elif self.state_FSM_request is NetRouter_Handler.states_FSM_request.sending:
				self.state_device = NetRouter_Handler.states_device.busy 
				if self.device.commandSend(bytes(requestString, encoding = "ascii")) is True:
					self.state_FSM_request = NetRouter_Handler.states_FSM_request.waiting_receive
				else:
					self.state_FSM_request = NetRouter_Handler.states_FSM_request.destroy
					
			elif self.state_FSM_request is NetRouter_Handler.states_FSM_request.waiting_receive:
				time.sleep(self.device.commandResponseTime)
				self.totalCommandResponseTime += self.device.commandResponseTime
				
				if self.totalCommandResponseTime > self.device.max_commandResponseTime:
					self.state_FSM_request = NetRouter_Handler.states_FSM_request.destroy
			
			elif self.state_FSM_request is NetRouter_Handler.states_FSM_request.receving:
				time.sleep(self.device.commandResponseTime)
				self.state_FSM_request = NetRouter_Handler.states_FSM_request.waiting_read
					
			elif self.state_FSM_request is NetRouter_Handler.states_FSM_request.waiting_read:
				self.state_device = NetRouter_Handler.states_device.response
				time.sleep(self.waitReadTime)
				self.state_FSM_request = NetRouter_Handler.states_FSM_request.destroy
						
			elif self.state_FSM_request is NetRouter_Handler.states_FSM_request.destroy:
				self.response.clear()
				self.totalCommandResponseTime = 0
				self.state_device = NetRouter_Handler.states_device.free 
				break
			
	def receiveFSM(self):
		while True:
			if self.state_FSM_receive is NetRouter_Handler.states_FSM_receive.disconnected:
				#change state to disconneced
				self.state_FSM_receive = NetRouter_Handler.states_FSM_receive.disconnected 
				self.state_FSM_request = NetRouter_Handler.states_FSM_request.disconnected 
				self.state_device = NetRouter_Handler.states_device.disconnected 
				
				# connect device
				if self.device.setup() is True:                                # device setup	
					#change state to connected
					self.state_FSM_receive = NetRouter_Handler.states_FSM_receive.listening 
					self.state_FSM_request = NetRouter_Handler.states_FSM_request.destroy 
					self.state_device = NetRouter_Handler.states_device.free
				else:
					time.sleep(self.hangupTime)
					
					
			elif self.state_FSM_receive is NetRouter_Handler.states_FSM_receive.listening:
				self.readString = self.device.commandRead()  # blocking for reading serial port

				if self.readString is None:                    # it means disconnected
					#change state 
					self.state_FSM_receive = NetRouter_Handler.states_FSM_receive.disconnected 
					self.state_FSM_request = NetRouter_Handler.states_FSM_request.disconnected 
					self.state_device = NetRouter_Handler.states_device.disconnected 
				else:
					#change state 
					self.state_FSM_receive = NetRouter_Handler.states_FSM_receive.received
			
			elif self.state_FSM_receive is NetRouter_Handler.states_FSM_receive.received:
				#print('raw: ',self.readString)
				receivePacket = self.device.Packet(str(self.readString,encoding = "utf-8"))

				if receivePacket is not None:
					if self.state_FSM_request is NetRouter_Handler.states_FSM_request.waiting_receive:
						self.state_FSM_request = NetRouter_Handler.states_FSM_request.receving
					if self.state_FSM_request is NetRouter_Handler.states_FSM_request.receving:
						self.response.append(receivePacket)
					self.processPacket(receivePacket)
					
				self.state_FSM_receive = NetRouter_Handler.states_FSM_receive.listening 

	

	
	def processPacket (self,packet):
		packetProcessDict={'RSSI':self.packetProcess_RSSI}
		
		try:
			packetProcessDict[packet.title](packet.content)
		except KeyError:
			pass

	def packetProcess_RSSI(self,content):
		self.rssi=int(content)
		
		
	
	

	


	


	
		
