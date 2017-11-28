from netRouter import NetRouter_Handler
from LTElocation import Location
import threading
import e3372_drive
import LTElocation
import time
import json
import paho.mqtt.client as mqtt

def init_mqtt():
	mqttClient.username_pw_set("radon_1", "qweasdzxc")  
	HOST = "108.61.171.128"
	mqttClient.connect(HOST, 1883, 60)
	mqttClient.loop_start()

def publish_location(mcc,mnc,lac,cid):
	data = [{'mcc':mcc,'mnc':mnc,'lac':lac,'cid':cid}]
	jsonString = json.dumps(data)
	mqttClient.publish("radon/1/location",jsonString)


hangup_time = 1 #s
location_update_time = 5 #s
mcc = 240
mnc = 1
LTE_Dongle = NetRouter_Handler(hangup_time,5,e3372_drive)
location = Location(LTE_Dongle,location_update_time,mcc,mnc)
mqttClient = mqtt.Client()
init_mqtt()

while True:
	print('dongle_request: ',LTE_Dongle.state_FSM_request)
	print('dongle_state: ',LTE_Dongle.state_device)
	print('location: ',location.state_FSM)
	print('-------')
	if location.lac != 0 and location.cid !=0:
		try:
			publish_location(mcc,mnc,location.lac,location.cid)
		except:
			try:
				init_mqtt()
			except:
				pass
			
	time.sleep(5)
	



	