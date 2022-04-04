# import the necessary packages
import json
import os
import random
import boto3

import cv2 as cv
import keras.backend as K
import numpy as np
import scipy.io

from utils import load_model
img_width, img_height = 224, 224
s3.download_file('electri-image-uploads','models/model.96-0.89.hdf5','/tmp/model.h5')
model = load_model()
model.load_weights('/tmp/model.h5')

cars_meta = scipy.io.loadmat('devkit/cars_meta')
class_names = cars_meta['class_names']  # shape=(1, 196)
class_names = np.transpose(class_names)
def handler(event, context):
    print(event)
    print(context)
    s3 = boto3.client('s3')
    path = event['preprocessed_image_path']
    print('Downloading image')
    s3.download_file('electri-image-uploads',path, '/tmp/img_foreground.png')
    bgr_img = cv.imread('/tmp/img_foreground.png')
    bgr_img = cv.resize(bgr_img, (img_width, img_height), cv.INTER_CUBIC)
    rgb_img = cv.cvtColor(bgr_img, cv.COLOR_BGR2RGB)
    rgb_img = np.expand_dims(rgb_img, 0)
    preds = model.predict(rgb_img)
    class_id = np.argmax(preds)
    make,model = class_names[class_id][0][0].split(' ',1)
    K.clear_session()
    return {'make': make,"model":model}