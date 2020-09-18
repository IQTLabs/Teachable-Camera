# Teachable Camera Detect

This folder contain the heart of Teachable Camera, the program which performs the object detection. It started from Google's [example code](https://github.com/google-coral/examples-camera/tree/master/opencv) for using [OpenCV](https://github.com/opencv/opencv) to perform object detection on camera images. OpenCV provides a flexible framework for ingesting video, formatting it and taking snapshots. It should support using RTSP IP Cameras, USB WebCams and the Coral Camera. 

This program has only be tested on the [Google Coral Dev Board](https://coral.ai/products/dev-board), but it should work on any platform that supports the Google Coral USB Accelerator.

## What it does

This program will save an image every time an object is detected. While the Coral Accelerator performs object detection at 30fps, an image will only be saved at a maximum rate of once per second to prevent storage from filling up. Using the **include** and **exclude** arguments (described) below, you can limit what types of objects trigger an image being saved. This makes it easy to build a dataset of images of a particular type of object. The images are saved into the `capture` directory in the root of the repo.

A JSON file is saved alongside each image. It an contains array of bounding boxes for all of the objects detected in an image. An example JSON file is below:
````
[{
	"bbox": {
		"top": 128,
		"left": 249,
		"width": 550,
		"height": 447
	},
	"label": "car",
	"prediction": 93
}, {
	"bbox": {
		"top": 0,
		"left": 706,
		"width": 313,
		"height": 280
	},
	"label": "truck",
	"prediction": 78
}]
````

The **top** and **left** coordinates for the bounding boxes are relative to the upper left hand corner of the image, measured in pixels.

### Webserver
The program includes a small Flask server that provides a stream of the images being captured with the detected objects overlaid. This image is progressively updated, providing a live view. The image is the only thing being served up by this server. The Flask server is available on port 8888. The Web App is provided by [**dashboard-serve**](../dashboard-serve/README.md) which serves a static version of [**dashboard**](../dashboard/README.md).

### MQTT
Everytime an object detection triggers an image being saved, an MQTT message is sent out on the **detection** topic. A small snapshot of that image is also sent out on the **detection-image** topic. Additionally, a count of each type of object currently being detected is sent out on a periodic basis on the **detection-count** topic. More details on the MQTT message and topic formats can be found in the [Main Readme](../README.md). Port 7447 is used to connect to the MQTT broker.

### Default model

By default, this uses the ```mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite``` model.

You can change the model and the labels file using flags ```--model``` and ```--labels```.

The model architecture is limited to what is supported by the Coral. It is probably best to stick with MobileNet.

## Arguments

*All of the arguments are optional and provide increasing control over the configuration*

 - **model** path to the model you want to use, defaults to COCO
 - **labels** labels for the model you are using, default to COCO labels
 - **top_k**  number of categories with highest score to display, defaults to 3
 - **threshold** classifier score threshold
 - **videosrc** what video source you want to use. Choices are `net` or `dev`. Default is `dev`:
    - **dev** a directly connected (dev) camera, can be Coral cam or USB cam or Networked 
    - **net** network video source, using RTSP. The --netsrc argument must be specified. 
	- **file** a video file can be used as a source
 - **camera_idx**  Index of which video source to use. I am not sure how OpenCV enumerates them. Defaults to 0.
 - **filesrc** the path to the video file. In the Docker container should be at /app/videos
 - **netsrc** If the `videosrc` is `net` then specify the URL. Example: `rtsp://192.168.1.43/mpeg4/media.amp`
 - **exclude** A comma separated list of objects to exclude from recording. If there is a space in the object label, enclose it in quotes.
  - **exclude** A comma separated list of objects to exclude from recording. If there is a space in the object label, enclose it in quotes.
 - **ip**  *type=str* ip address of the device, default='127.0.0.1'
 - **port** *type=int* ephemeral port number of the server (1024 to 65535), default=8888
 
## Using Docker Containers

While this program can be run normally from the command line, it is designed to be run inside a Docker container. Docker-Compose is the best way to orchestrate building and running all of the containers for the project. It is described in the [main Readme](../README.md). When running inside a container, make sure to use the Python `-u` flag so that print() statements are shown.

Build:
`docker build -t capture .`

Run: 
`docker run --privileged -it -p 8888:8888 -p 7447:7447 capture /bin/bash`

## Example Commands:

If you want to run the program directly from the command, the following are some example configurations we have used:

- `python3 detect.py --videosrc=net --netsrc=rtsp://192.168.1.43/mpeg4/media.amp`
- `python3 detect.py --videosrc=net --netsrc=rtsp://192.168.1.43/mpeg4/media.amp --top_k=10 --threshold=0.2`
- `python3 detect.py --videosrc=net --netsrc=rtsp://192.168.1.43/mpeg4/media.amp --top_k=10 --threshold=0.4 --exclude=person,car`
- `python3 detect.py --videosrc=net --netsrc=rtsp://192.168.1.202/img/video.sav --top_k=10 --threshold=0.45 --exclude=person,car`
- `python3 detect.py --videosrc=net --netsrc=rtsp://192.168.1.43/mpeg4/media.amp --top_k=10 --threshold=0.4 --exclude=person,car,"traffic light" --srcsize=1024,768`
- `python3 detect.py --videosrc=net --netsrc=rtsp://192.168.1.202/img/video.sav --top_k=10 --threshold=0.60 --exclude=person,car,traffic\ light,fire\ hydrant`
