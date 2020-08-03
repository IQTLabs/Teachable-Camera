import paho.mqtt.client as mqtt #import the client1
import time
import sys
#from cryptography.fernet import Fernet
import random
import serial
import os

Unit = 'Local'

#######################################################
##                Initialize Variables               ##
#######################################################
ser = serial.Serial()
uuidCoral = os.getenv('SB1_SHORT_DEVICE_ID')
mqttPublicBroker = os.getenv('SB1_MQTT_PUBLIC_ADDRESS')
mqttKey = os.getenv('SB1_MQTT_KEY')

serialPort = '/dev/ttyACM0'

if sys.argv[2:]:
      serialPort = sys.argv[2]

config = {}
config['Local'] = ["127.0.0.1", "/eyeqt/+/detect", 'localhost, for onboard system monitoring']
config['Public'] = ["broker.hivemq.com", mqttPublicBroker, 'Public MQTT Bus Monitoring']
timeTrigger = 0
key = mqttKey
#f = Fernet(key)
ID = str(random.randint(1,100001))
        
### Serial Port Setup ###
ser.port = serialPort #get port from CLI argument (default is /dev/ttyACM0)
ser.baudrate = 115200
ser.bytesize = 8
ser.parity = 'N'
ser.stopbits = 1

if ser.isOpen():
   ser.close()

os.system('sudo chmod 777 %s' % ser.portstr)
ser.open()
print("Opening LoRa Radio on:",ser.portstr)
ser.flushInput()
ser.flushOutput()
### End Serial Port Setup ###

def printHelp():
    print('Command Syntax:    monitor.py <MQTT Bus Name> <serial port (default:/dev/ttyACM0)>')
    print('Example: monitor.py Local /dev/ttyACM0)')
    print('Function will not execute without specifying a valid MQTT Bus Name.  Valid names are:')
    for name in config.keys():
        print('   - '+name+': '+config[name][2])

#def sendMessage(channel, message):
    #if Unit=='Public':
        #message = f.encrypt(message.encode())
    #client.publish(topic+"/"+channel,message)
        
#############################################
##         MQTT Callback Function          ##
#############################################
def on_message(client, userdata, message):
    command = str(message.payload.decode("utf-8"))
    print(message.topic+':'+command)
    stringV1="{} got alert".format(uuidCoral)
    ser.flushOutput()		 #Clear output buffer
    ser.write(stringV1.encode()) #send it to LoRa radio

#############################################
##     Public MQTT Callback Function       ##
#############################################
def on_message_public(client, userdata, message):
    command = str(f.decrypt(message.payload).decode("utf-8"))
    print(message.topic+':'+command)

if len(sys.argv)<2:
    printHelp()
    exit()
elif sys.argv[1] not in config.keys():
    printHelp()
    print(sys.argv[1] + ' is an invalid MQTT Bus Name')
    exit()

#############################################
##       Initialize Local MQTT Bus         ##
#############################################
Unit = sys.argv[1]
broker_address=config[Unit][0]
topic= config[Unit][1]
print("connecting to MQTT broker at "+broker_address+", channel '"+topic+"'")
client = mqtt.Client("Monitor-"+Unit+"-"+ID) #create new instance

if Unit=='Public':
    client.on_message=on_message_public
else:
    client.on_message=on_message #attach function to callback

client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
client.subscribe(topic+"/#")
#sendMessage("registration", "Monitor-"+Unit+"-"+ID+" Registration")

#############################################
##                Main Loop                ##
#############################################
while True:
    if timeTrigger < time.mktime(time.gmtime()):
        timeTrigger = time.mktime(time.gmtime()) + 60
        #sendMessage("heartbeat", "Monitor-"+Unit+"-"+ID+" Heartbeat")
        stringV1="Heartbeat"
        ser.write(stringV1.encode()) #send it to LoRa radio
    time.sleep(0.005)
