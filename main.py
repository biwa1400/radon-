from netRouter import NetRouter_Handler
import e3372_drive
import time

LTE_Dongle = NetRouter_Handler(1,e3372_drive)
while True:
	print(LTE_Dongle.state)
	time.sleep(1)
	