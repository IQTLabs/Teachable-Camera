#!/bin/bash

#source this script to set env variables
#Version 0.3 June 2020
#Version 0.5 July 2020

#Set file name and install PATH
_FILE=sb1IdInit.env
ENV_PATH=./
ENV_FILE=${ENV_PATH}${_FILE}

#Get wired MAC daddy
IFACE1=eth0
read _MAC < /sys/class/net/$IFACE1/address
MAC1=${_MAC:0:2}${_MAC:3:2}${_MAC:6:2}${_MAC:9:2}${_MAC:12:2}${_MAC:15:2}

#Get wireless MAC
IFACE2=wlan0
read _MAC < /sys/class/net/$IFACE2/address
MAC2=${_MAC:0:2}${_MAC:3:2}${_MAC:6:2}${_MAC:9:2}${_MAC:12:2}${_MAC:15:2}

#Get hostname
read SB1_HOSTNAME < /etc/hostname

#Heartbeat in seconds
SB1_HEARTBEAT_DURATION=60

#LoRa ID - 4 Bytes (32 bits)
LORA_ID_H=dead
LORA_ID_L=beef
SB1_LORA_ID=${LORA_ID_H}${LORA_ID_L}

#Generate Long ID - 16 Bytes (128 bits)
SB1_LONG_DEVICE_ID=${MAC1}${MAC2}${SB1_LORA_ID}

#Generate Short ID - 4 Bytes (32 bits)
SB1_SHORT_DEVICE_ID=${MAC1:10:2}${MAC2:10:2}${LORA_ID_L}

#MQTT Stuff
SB1_MQTT_PUBLIC_ADDRESS=deaddead
SB1_MQTT_KEY=beefbeef

#Export everybody
export SB1_HOSTNAME
export SB1_HEARTBEAT_DURATION
export SB1_LORA_ID
export SB1_LONG_DEVICE_ID
export SB1_SHORT_DEVICE_ID
export SB1_MQTT_PUBLIC_ADDRESS
export SB1_MQTT_KEY

#Parse command line args
for var in "$@"
do
key="$1"

case $key in
	-v)
	echo "Iface: $IFACE1 MAC: $MAC1"
	echo "Iface: $IFACE2 MAC: $MAC2"
	echo "SB1_HOSTNAME=$SB1_HOSTNAME"
	echo "SB1_HEARTBEAT_DURATION=$SB1_HEARTBEAT_DURATION"
	echo "SB1_LORA_ID=$SB1_LORA_ID"
	echo "SB1_LONG_DEVICE_ID=$SB1_LONG_DEVICE_ID"
	echo "SB1_SHORT_DEVICE_ID=$SB1_SHORT_DEVICE_ID"
	shift
	;;
	-h)
	echo "Useage: sb1IdInit.sh [-v] [-h]"
	echo "-v:  verbose, shows output"
	echo "-h:  help, shows this help"
	exit
	;;
esac
done

#Check for existing file
if test -f "$ENV_FILE" ; then
	echo "Envoronment file $ENV_FILE exists - overwriting!"
	echo "SB1_HOSTNAME=$SB1_HOSTNAME" > $ENV_FILE
	echo "SB1_HEARTBEAT_DURATION=$SB1_HEARTBEAT_DURATION"  >> $ENV_FILE
	echo "SB1_LORA_ID=$SB1_LORA_ID"  >> $ENV_FILE
	echo "SB1_LONG_DEVICE_ID=$SB1_LONG_DEVICE_ID" >> $ENV_FILE
	echo "SB1_SHORT_DEVICE_ID=$SB1_SHORT_DEVICE_ID" >> $ENV_FILE
else
	echo "Creating environment file $ENV_FILE"
	touch $ENV_FILE
	echo "SB1_HOSTNAME=$SB1_HOSTNAME" > $ENV_FILE
	echo "SB1_HEARTBEAT_DURATION=$SB1_HEARTBEAT_DURATION"  >> $ENV_FILE
	echo "SB1_LORA_ID=$SB1_LORA_ID"  >> $ENV_FILE
	echo "SB1_LONG_DEVICE_ID=$SB1_LONG_DEVICE_ID" >> $ENV_FILE
	echo "SB1_SHORT_DEVICE_ID=$SB1_SHORT_DEVICE_ID" >> $ENV_FILE
fi
