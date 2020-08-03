import paho.mqtt.client as mqtt
import time
import os

uuid = str(os.getenv('SB1_LONG_DEVICE_ID'))
remoteIP = str(os.getenv('REMOTE_MQTT_IP'))

#######################################################
##                Initialize Variables               ##
#######################################################
config = {}
config['Local'] = ["127.0.0.1", "/eyeqt]
timeTrigger = 0
Active = True


def on_disconnect(client, userdata, rc):
    global Active
    Active = False


#######################################################
##           Local MQTT Callback Function            ##
#######################################################
def on_message_local(client, userdata, message):
    ignoreTopics = ['heartbeat','Heartbeat','registration','response','command-response']
    command = str(message.payload.decode("utf-8"))
    if message.topic.split('/')[-1] not in ignoreTopics:
        print(message.topic+':'+command)
        clientPublic.publish(public_topic+"/inbound/"+uuid+"/"+message.topic.split('/')[-1],command)


#######################################################
##           Public MQTT Callback Function           ##
#######################################################
def on_message_public(client, userdata, message):
    ignoreTopics = ['heartbeat','registration','response','command-response']
    command = str(message.payload.decode("utf-8"))
    if message.topic.split('/')[1] == "outbound":
        print(message.topic+':'+command)


#############################################
##       Initialize Local MQTT Bus         ##
#############################################
Unit = 'Local'
broker_address=config[Unit][0]
local_topic= config[Unit][1]
print("connecting to MQTT broker at "+broker_address+", channel '"+local_topic+"'")
clientLocal = mqtt.Client(uuid) #create new instance
clientLocal.on_message=on_message_local #attach function to callback
clientLocal.on_disconnect = on_disconnect
clientLocal.connect(broker_address) #connect to broker
clientLocal.loop_start() #start the loop
clientLocal.subscribe(local_topic+"/#")
clientLocal.publish(local_topic+"/registration",uuid+": Relay Registration")


#############################################
##       Initialize Public MQTT Bus        ##
#############################################
Unit = 'Cap'
public_broker_address=config[Unit][0]
public_topic= config[Unit][1]
print("connecting to MQTT broker at "+public_broker_address+", channel '"+public_topic+"'")
clientPublic = mqtt.Client(uuid) #create new instance
clientPublic.on_message=on_message_public #attach function to callback
clientPublic.on_disconnect = on_disconnect
clientPublic.connect(public_broker_address) #connect to broker
clientPublic.loop_start() #start the loop
clientPublic.subscribe(public_topic+"/outbound")
clientPublic.publish(public_topic+"/registration",uuid+": Relay Registration")


#############################################
##                Main Loop                ##
#############################################
while Active:
    if timeTrigger < time.mktime(time.gmtime()):
        timeTrigger = time.mktime(time.gmtime()) + 60
        clientLocal.publish(local_topic+"/heartbeat",uuid+": Relay Heartbeat")
        clientPublic.publish(public_topic+"/heartbeat",uuid+": Relay Heartbeat")
    time.sleep(0.001)
