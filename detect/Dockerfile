##EdgeTPU Python does not work with Ubuntu 20.04 because it includes python 3.8 and the lib < 3.8
FROM ubuntu:18.04

RUN export DEBIAN_FRONTEND="noninteractive" && export TZ="America/New_York" \
    && apt-get update \
    && apt-get install -y \
        tzdata \
        nano \
        libhdf5-1* \
        python3 \
        python3-dev \
        python3-pip \
        python3-numpy \
        python3-opencv \
        python3-pil \
        curl \
        gnupg2 \
        apt-transport-https \
        ca-certificates \
        apt-utils \
    && rm -rf /var/lib/apt/lists/*

RUN  echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
    && apt-get update \
    && apt-get install -y python3-edgetpu libedgetpu1-std \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install flask imutils paho-mqtt
#TFLite runtime for PYthon 3.6 - from here: https://www.tensorflow.org/lite/guide/python
RUN pip3 install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp36-cp36m-linux_aarch64.whl
RUN mkdir -p /app/capture
WORKDIR /app

COPY *.tflite /app/
COPY *.txt /app/
COPY *.py /app/

