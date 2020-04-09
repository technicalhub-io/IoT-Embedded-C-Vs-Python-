import network
from umqtt.simple import MQTTClient
import machine
import time
import ubinascii
global rec_msg
rec_msg = None
CONFIG = {
     # Configuration details of the MQTT broker

     "MQTT_BROKER": "test.mosquitto.org",

     "USER": "",

     "PASSWORD": "",

     "PORT": 1883,

     "TOPIC": b"sub_data",

     "CLIENT_ID": b"esp8266_" + ubinascii.hexlify(machine.unique_id())
}

# For WiFi Connection.
station=network.WLAN(network.STA_IF)
station.active(True)
station.connect("MOBIE", "123456789")

while (not (station.isconnected())):

        print("waiting to Connect")

        print (station.ifconfig())

        time.sleep(1)

station.ifconfig()
print ("Connected")
print("Connected to Wifi\n")

def listen():
    global rec_msg
    client = MQTTClient(CONFIG['CLIENT_ID'], CONFIG['MQTT_BROKER'], port=CONFIG['PORT'])

    client.set_callback(onMessage)

    client.connect()

    client.publish("data", "ESP8266 is Connected")
    print(b"esp8266_" + ubinascii.hexlify(machine.unique_id()))
    client.subscribe(CONFIG['TOPIC'])

    print("ESP8266 is Connected to %s and subscribed to %s topic" % (CONFIG['MQTT_BROKER'], CONFIG['TOPIC']))

    try:

        while True:
            global rec_msg
            msg = client.wait_msg()
            if rec_msg is not None:
                client.publish("data", "ESP8266 is Recieved")
                rec_msg = None
    finally:
        client.disconnect()

def onMessage(topic, msg):

    print("Topic: %s, Message: %s" % (topic, msg))
    global rec_msg
    rec_msg = msg

listen()
