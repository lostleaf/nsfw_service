import caffe
import numpy as np
import requests
import os
import datetime
from cStringIO import StringIO
from classify_nsfw import caffe_preprocess_and_compute
from flask import Flask, request, jsonify, abort
from PIL import Image

MISTAKE_STORAGE = "mistakes/"

class NSFWDetector:

    def __init__(self):
        self.nsfw_net = caffe.Net("nsfw_model/deploy.prototxt", "nsfw_model/resnet_50_1by2_nsfw.caffemodel", caffe.TEST)
        # The following preprocessing settings are required by the model itself
        self.caffe_transformer = caffe.io.Transformer({'data': self.nsfw_net.blobs['data'].data.shape})
        self.caffe_transformer.set_transpose('data', (2, 0, 1))  # move image channels to outermost
        self.caffe_transformer.set_mean('data', np.array([104, 117, 123]))  # subtract the dataset-mean value in each channel
        self.caffe_transformer.set_raw_scale('data', 255)  # rescale to [0, 255]
        self.caffe_transformer.set_channel_swap('data', (2, 1, 0))  # swap channels from RGB to BGR
    
    def detect_image(self, image_data):
        scores = caffe_preprocess_and_compute(image_data, 
                                              caffe_transformer=self.caffe_transformer, 
                                              caffe_net=self.nsfw_net, 
                                              output_layers=['prob'])
        return scores[1]


def save_image(image, image_class):
    image_class = bool(image_class)
    save_folder = os.path.join(MISTAKE_STORAGE, str(image_class))
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d.%H:%M:%S")
    image.save(os.path.join(save_folder, current_time + ".png"), "PNG")


app = Flask(__name__, static_url_path='')
detector = NSFWDetector()


@app.route("/query", methods=["POST"])
def query():
    json_query = request.get_json()
    results = []
    for image_url in json_query:
        response = requests.get(image_url)
        if response.status_code == requests.codes.ok:
            image_data = response.content
            results.append(detector.detect_image(image_data))
        else:
            results.append(None)
    return jsonify(results)


@app.route("/report_mistake", methods=["POST"])
def report_mistake():
    json_request = request.get_json()
    results = []
    for image_url, image_class in json_request:
        response = requests.get(image_url)
        if response.status_code == requests.codes.ok:
            image = Image.open(StringIO(response.content))
            save_image(image, image_class)
            results.append(True)
        else:
            results.append(False)
    return jsonify(results)

@app.route("/")
def root():
    return app.send_static_file("README.html")
