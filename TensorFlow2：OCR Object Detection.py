import os
import cv2
import tensorflow as tf
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

import imutils

import argparse
import time
import sys
sys.path.append("..")

from utils import label_map_util
from utils import visualization_utils as vis_utils

MODEL_Name = 'inference_graph'
CWD_PATH = os.getcwd()

PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_Name, 'frozen_inference_graph.pb')
PATH_TO_LABELS = os.path.join(CWD_PATH, 'training', 'labelmap.pbtxt')

NUM_CLASSES = 2

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

detection_graph = tf.Graph()

with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.Gfile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def(od_graph_def, name='')
    sess = tf.Session(graph=detection_graph)

