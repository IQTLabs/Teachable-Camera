FROM alpine:3.9

ARG TIMEZONE=America/New_York

RUN 	apk add --no-cache python3 python3-dev \
	&& pip3 install --no-cache-dir paho-mqtt pyserial \ 
        && rm -rf /var/cache/apk/*

COPY monitor.py monitor.py

ENTRYPOINT python3 monitor.py Local

### docker run --detach --restart unless-stopped --device=/dev/ttyACM0 --network="host" --name gcode-receive mchadwick/gcode-receiver:latest
