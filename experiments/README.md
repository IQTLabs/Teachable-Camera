# Teachable Camera Evaluation Experiments

This repo enables analysis of Teachable Camera model performance. In particular, the images and scripts let an analyst determine via in-depth review the extent to which a trained Teachable Camera model is performing object detection adequately.

Step 1. Install the required packages, if needed.

```bash
Install TensorFlow Lite interpretor using instructions from this link - https://www.tensorflow.org/lite/guide/python
sudo pip3 install Pillow
sudo pip3 install opencv-python
```

Step 2. Run this script to create images with overlaid bounding boxes.

```bash
sudo python3 detect-bbox.py \
     --model <tflite model path> \
     --labels <label file> \
     --top_k <number of categories with highest score> \
     --threshold <classifier score threshold> \
     --images <directory name containing images>
```

## Default Values

The default images directory is the current directory.

The model can be run with default values of model, label, top_k and threshold values as shown below: 

- model = output_tflite_graph.tflite
- labels = labels.txt
- images = evaluation-images
- top_k = 3
- threshold = 0.1

For example, to run the detect-bbox.py script with no arguments:

```bash
sudo python3 detect-bbox.py   
```

Alternatively, a user could pass a different images directory:

```bash
sudo python3 detect-bbox.py --images trucks-in-the-wild
```
