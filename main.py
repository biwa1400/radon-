from netRouter import NetRouter_Handler
from LTElocation import Location
import threading
import e3372_drive
import LTElocation
import time
import json
import paho.mqtt.client as mqtt

def init_mqtt():
	while True:
		try:
			mqttClient.username_pw_set("radon_1", "qweasdzxc")  
			HOST = "m23.cloudmqtt.com"
			mqttClient.connect(HOST, 11112, 5)
			mqttClient.loop_start()
			break
		except:
			print ("in init except")
			time.sleep(5)

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
			print("in mqtt send")
			publish_location(mcc,mnc,location.lac,location.cid)
		except:
			print ("in send except")
			init_mqtt()

	time.sleep(5)
	



	
