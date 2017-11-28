import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
	pass


client = mqtt.Client()
client.username_pw_set("radon_1", "qweasdzxc")  # 必须设置，否则会返回「Connected with result code 4」
client.on_connect = on_connect
client.on_message = on_message
HOST = "108.61.171.128"
client.connect(HOST, 1883, 60)
client.user_data_set('binya')
client.loop_start()

while True:
	client.publish("radon/1/location",'radon')
	print('send')
	time.sleep(5)