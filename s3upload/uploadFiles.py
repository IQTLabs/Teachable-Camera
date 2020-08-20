import paho.mqtt.client as mqtt #import the client1
import time
import random
import socket
import os
import sys
import s3upload as s3
uuidCoral = str(os.getenv('MAC1'))


Active = True
Unit = 'Local'

#######################################################
##                Initialize Variables               ##
#######################################################
config = {}
config['Local'] = ["127.0.0.1", "/upload", "Receive Commands on MQTT"]
hostname=socket.gethostname()
timeTrigger = 0
ID = str(random.randint(1,100001))

#######################################################
##           Local MQTT Callback Function            ##
#######################################################
def on_message_local(client, userdata, message):
    payload = str(message.payload.decode("utf-8"))
    print('Message Received: ' + message.topic + ' | ' + payload)


def on_disconnect(client, userdata, rc):
    global Active
    Active = False


#############################################
##       Initialize Local MQTT Bus         ##
#############################################
broker_address=config[Unit][0]
local_topic= '/teachable-camera'+config[Unit][1]
print("connecting to MQTT broker at "+broker_address+", channel '"+local_topic+"'")
clientLocal = mqtt.Client("S3-Upload-"+ID) #create new instance
clientLocal.on_message = on_message_local #attach function to callback
clientLocal.on_disconnect = on_disconnect
clientLocal.connect(broker_address) #connect to broker
clientLocal.loop_start() #start the loop
clientLocal.subscribe(local_topic+"/receive/#")
clientLocal.publish(local_topic+"/registration","S3-Upload-"+ID+" Receiver Registration")

#############################################
##                Main Loop                ##
#############################################
while Active:
    if timeTrigger < time.mktime(time.gmtime()):
        timeTrigger = time.mktime(time.gmtime()) + 10
        clientLocal.publish(local_topic+"/Heartbeat","Lamp-Control-"+ID+" Heartbeat")
    for file in os.listdir(s3.image_path):
        if file.split('.')[1] == 'jpeg':
            file_full_path = os.path.join(s3.image_path, file)
            print(file_full_path)
            if os.path.exists(file_full_path.replace('jpeg','json')):
                time.sleep(0.5)  # bug fix - adding delay to ensure the json file has been fully written
                response = s3.uploadImage(file_full_path, file_full_path.replace('jpeg','json'))
                clientLocal.publish(local_topic, response)
    time.sleep(0.1)
