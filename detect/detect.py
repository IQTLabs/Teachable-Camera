# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo that runs object detection on camera frames using OpenCV.

TEST_DATA=../all_models

Run face detection model:
python3 detect.py \
  --model ${TEST_DATA}/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite

Run coco model:
python3 detect.py \
  --model ${TEST_DATA}/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite \
  --labels ${TEST_DATA}/coco_labels.txt

"""
import argparse
import collections
import common
import cv2
import time
from datetime import datetime
import errno
import numpy as np
import os, io, sys
from PIL import Image
import json
import re
import tflite_runtime.interpreter as tflite
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import imutils
import time
from time import sleep
import cv2
import paho.mqtt.client as mqtt #import the client1
import random
Unit = 'Local'

# Use SB device short ID
uuidCoral = os.getenv('SB1_SHORT_DEVICE_ID')

#######################################################
##                Initialize Variables               ##
#######################################################
config = {}
config['Local'] = ["127.0.0.1", "/detect", "Receive Commands on MQTT"]
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
local_topic= '/teachable-camera/' + uuidCoral #+ '/detect'
print("connecting to MQTT broker at "+broker_address+", channel '"+local_topic+"'")
processName = "Detect-"+ID
clientLocal = mqtt.Client(processName) #create new instance
clientLocal.on_message = on_message_local #attach function to callback
clientLocal.on_disconnect = on_disconnect
clientLocal.connect(broker_address) #connect to broker
clientLocal.loop_start() #start the loop
clientLocal.subscribe(local_topic+"/receive/#")
clientLocal.publish(local_topic+"/registration",processName + " Detector Registration")

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()
# initialize a flask object
app = Flask(__name__)
Object = collections.namedtuple('Object', ['id', 'score', 'bbox'])
last_save = time.time()
last_count = time.time()



def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while True:
        
        # This is how you set the frames per second... crude
        sleep(0.20)

        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # ensure the frame was successfully encoded
            
            if not flag:
                continue 
        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed.jpg")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    print("video feed req")
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

def load_labels(path):
    p = re.compile(r'\s*(\d+)(.+)')
    with open(path, 'r', encoding='utf-8') as f:
       lines = (p.match(line).groups() for line in f.readlines())
       return {int(num): text.strip() for num, text in lines}

class BBox(collections.namedtuple('BBox', ['xmin', 'ymin', 'xmax', 'ymax'])):
    """Bounding box.
    Represents a rectangle which sides are either vertical or horizontal, parallel
    to the x or y axis.
    """
    __slots__ = ()

def get_output(interpreter, score_threshold, top_k, image_scale=1.0):
    """Returns list of detected objects."""
    boxes = common.output_tensor(interpreter, 0)
    class_ids = common.output_tensor(interpreter, 1)
    scores = common.output_tensor(interpreter, 2)
    count = int(common.output_tensor(interpreter, 3))

    def make(i):
        ymin, xmin, ymax, xmax = boxes[i]
        return Object(
            id=int(class_ids[i]),
            score=scores[i],
            bbox=BBox(xmin=np.maximum(0.0, xmin),
                      ymin=np.maximum(0.0, ymin),
                      xmax=np.minimum(1.0, xmax),
                      ymax=np.minimum(1.0, ymax)))

    return [make(i) for i in range(top_k) if scores[i] >= score_threshold]

def detect_object(args):
    global outputFrame, lock

    interpreter = common.make_interpreter(args.model)
    interpreter.allocate_tensors()
    labels = load_labels(args.labels)

    if args.videosrc=='dev': 
        cap = cv2.VideoCapture(args.camera_idx)
    elif args.videosrc=='file':
        cap = cv2.VideoCapture(args.filesrc)    
    else:
        if args.netsrc==None:
            print("--videosrc was set to net but --netsrc was not specified")
            sys.exit()
        cap = cv2.VideoCapture(args.netsrc)        
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT) 
    frame_count = 0
    while cap.isOpened():

        (grabbed, frame) = cap.read()

        if not grabbed and args.videosrc=='file':
            cap = cv2.VideoCapture(args.filesrc)
            continue          

        cv2_im = frame

        cv2_im_rgb = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im_rgb)
        snapshot_im = pil_im
        common.set_input(interpreter, pil_im)
        interpreter.invoke()
        objs = get_output(interpreter, score_threshold=args.threshold, top_k=args.top_k)
        cv2_im = append_objs_to_img(cv2_im, objs, labels)
        if args.displayBool == 'True':
            cv2.imshow('frame', cv2_im)

        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame = cv2_im.copy()


        if (time.time() - last_save) >=1:
            take_snapshot(snapshot_im, objs, labels, exclude=args.exclude.split(','), include=args.include.split(','))
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    default_model_dir = './'
    default_model = 'mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite'
    default_labels = 'coco_labels.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='.tflite model path',
                        default=os.path.join(default_model_dir,default_model))
    parser.add_argument('--labels', help='label file path',
                        default=os.path.join(default_model_dir, default_labels))
    parser.add_argument('--top_k', type=int, default=3,
                        help='number of categories with highest score to display')
    parser.add_argument('--camera_idx', type=int, help='Index of which video source to use. ', default = 0)
    parser.add_argument('--threshold', type=float, default=0.1,
                        help='classifier score threshold')
    parser.add_argument('--videosrc', help='Directly connected (dev) or Networked (net) video source. ', choices=['dev','net','file'],
                        default='dev')
    parser.add_argument('--displayBool', help='Is a display attached',
                        default='False',
                        choices=['True', 'False'])
    parser.add_argument('--netsrc', help="Networked video source, example format: rtsp://192.168.1.43/mpeg4/media.amp",)
    parser.add_argument('--filesrc', help="Video file source. The videos subdirectory gets mapped into the Docker container, so place your files there.",)
    
    parser.add_argument('--exclude', help='A comma seperated list of objects that do not trigger a capture',
                        default='')
    parser.add_argument('--include', help='A comma seperated list of objects that trigger a capture',
                        default='')
    args = parser.parse_args()
    print(args)
    print('Loading {} with {} labels.'.format(args.model, args.labels))


    # start a thread that will perform motion detection
    t = threading.Thread(target=detect_object, args=(
        args,))
    t.daemon = True
    t.start()


    app.run(host="0.0.0.0", port=8888, debug=True,
        threaded=True, use_reloader=False)

 



def append_objs_to_img(cv2_im, objs, labels):
    height, width, channels = cv2_im.shape
    for obj in objs:
        x0, y0, x1, y1 = list(obj.bbox)
        x0, y0, x1, y1 = int(x0*width), int(y0*height), int(x1*width), int(y1*height)
        percent = int(100 * obj.score)
        label = '{}% {}'.format(percent, labels.get(obj.id, obj.id))

        cv2_im = cv2.rectangle(cv2_im, (x0, y0), (x1, y1), (0, 255, 0), 2)
        cv2_im = cv2.putText(cv2_im, label, (x0, y0+30),
                             cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
    return cv2_im

def pil_image_to_byte_array(image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, "JPEG")
    return imgByteArr.getvalue()

def take_snapshot(snapshot_im, objs, labels, exclude, include):
    global last_save
    global last_count
    global local_topic
    width, height = snapshot_im.size
    take_snapshot = False
    interesting_objects = []
    
    bounding_boxes = []
    object_count = {}

    for obj in objs:
        x0, y0, x1, y1 = list(obj.bbox)
        x0, y0, x1, y1 = int(x0*width), int(y0*height), int(x1*width), int(y1*height)
        x, y, w, h = x0, y0, x1 - x0, y1 - y0

        percent = int(100 * obj.score)
        label = labels.get(obj.id, obj.id)
        
        if not label in object_count:
            object_count[label] = 1
        else:
            object_count[label] += 1
        #label = '{}% {}'.format(percent, labels.get(obj.id, obj.id))
        bbox = {}
        bbox["top"] = y
        bbox["left"] = x
        bbox["width"] = w
        bbox["height"] = h
        bounding_boxes.append({"bbox": bbox,
                    "label": label,
                    "prediction": percent
                    })
        if include[0]:
            if label in include:
                take_snapshot = True
                interesting_objects.append(label)
                print("{} {}%".format(label,percent))
        else:
            if label not in exclude:
                take_snapshot = True
                interesting_objects.append(label)
                print("{} {}%".format(label,percent))
    if (time.time() - last_count) >=10:
        last_count = time.time()
        clientLocal.publish(local_topic+"/detection-count",json.dumps(object_count))
    if take_snapshot:
        last_save = time.time()
        mydir = "/app/capture"
        try:
            os.makedirs(mydir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise  # This was not a "directory exist" error..
        width, height = snapshot_im.size
        ratio = width/200
        newsize = (int(width/ratio), int(height/ratio))
        mqtt_im = snapshot_im.resize(newsize)
        mqtt_byte = pil_image_to_byte_array(mqtt_im)
        mqtt_message = {  "objects": interesting_objects}
        mqtt_json=json.dumps(mqtt_message)
        clientLocal.publish(local_topic+"/detection-image",mqtt_byte)
        clientLocal.publish(local_topic+"/detection",mqtt_json)
        filename = "{}/{}_{}_{}".format(mydir,uuidCoral,datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),'-'.join(interesting_objects))
        snapshot_im.save("{}.jpeg".format(filename))
        json_filename = filename + ".json"
        with open(json_filename, 'w') as outfile:
            json.dump(bounding_boxes, outfile)


if __name__ == '__main__':
    main()
