FROM alpine:3.9

ARG TIMEZONE=America/New_York

RUN apk add --no-cache git python3 ca-certificates libffi-dev && \
    apk add --no-cache --virtual=build-dependencies gcc musl-dev tzdata openssl-dev build-base linux-headers python3-dev && \
    cp "/usr/share/zoneinfo/${TIMEZONE}" /etc/localtime && echo "${TIMEZONE}" > /etc/timezone && \
    pip3 install --upgrade --no-cache-dir pip && \
    pip3 install --no-cache-dir paho-mqtt requests cffi smbus-cffi && \
    apk del build-dependencies && \
    rm -rf /tmp/* /var/tmp/* /var/cache/apk/*

COPY relay.py relay.py /app/

ENTRYPOINT python3 /app/relay.py

