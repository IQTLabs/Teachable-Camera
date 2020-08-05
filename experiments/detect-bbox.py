import common
import argparse
from PIL import Image
import cv2
import re
import collections
import numpy as np
import glob
from pathlib import Path
import os
import shutil

class BBox(collections.namedtuple('BBox', ['xmin', 'ymin', 'xmax', 'ymax'])):
    """Bounding box.
    Represents a rectangle which sides are either vertical or horizontal, parallel
    to the x or y axis.
    """
    __slots__ = ()

Object = collections.namedtuple('Object', ['id', 'score', 'bbox'])

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



def load_labels(path):
    p = re.compile(r'\s*(\d+)(.+)')
    with open(path, 'r', encoding='utf-8') as f:
       lines = (p.match(line).groups() for line in f.readlines())
       return {int(num): text.strip() for num, text in lines}

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

def detect_objects(args):
   interpreter = common.make_interpreter(args.model)
   interpreter.allocate_tensors()
   labels = load_labels(args.labels)
   dirname = args.images

   dirpath = Path('results/'+dirname)
   if dirpath.exists() and dirpath.is_dir():
       shutil.rmtree(dirpath)
   Path("results/"+dirname).mkdir(parents=True, exist_ok=True)

   for filename in glob.glob(dirname+"/*.jpeg"):
       print(filename)
       name = os.path.basename(filename)
       pil_im = Image.open(filename)
       open_cv_image = np.array(pil_im) 
       snapshot_im = pil_im
       common.set_input(interpreter, pil_im)
       interpreter.invoke()
       objs = get_output(interpreter, score_threshold=args.threshold, top_k=args.top_k)
       #print(objs)
       open_cv_image = append_objs_to_img(open_cv_image, objs, labels)
       cv2_im_rgb = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB)
       (flag, encodedImage) = cv2.imencode(".jpeg", cv2_im_rgb)
       #print(flag)
       #print(encodedImage)
       f = open("./results/"+dirname+"/"+name, "wb")
       f.write(encodedImage)
       f.close()

def main():
    default_model_dir = './'
    default_model = 'output_tflite_graph.tflite'
    default_labels = 'labels.txt'
    default_imageDir = 'evaluation-images'
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='.tflite model path',
                        default=os.path.join(default_model_dir,default_model))
    parser.add_argument('--labels', help='label file path',
                        default=os.path.join(default_model_dir, default_labels))
    parser.add_argument('--images', help='images directory name',
                        default=os.path.join(default_model_dir, default_imageDir))
    parser.add_argument('--top_k', type=int, default=3,
                        help='number of categories with highest score to display')
    parser.add_argument('--threshold', type=float, default=0.1,
                        help='classifier score threshold')
    args = parser.parse_args()
    print(args)
    print('Loading {} with {} labels.'.format(args.model, args.labels))
    detect_objects(args)

if __name__ == '__main__':
    main()

