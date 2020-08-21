FROM alpine:3.9

ARG TIMEZONE=America/New_York

RUN 	apk add --no-cache python3 python3-dev \
	&& pip3 install --no-cache-dir paho-mqtt pyserial \ 
        && rm -rf /var/cache/apk/*

COPY monitor.py monitor.py

ENTRYPOINT python3 monitor.py Local

