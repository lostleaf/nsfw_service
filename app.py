from flask import Flask, request, jsonify
import caffe

class NSFWDetector

    def __init__(self):
        self.nsfw_net = caffe.Net("deploy.prototxt", "resnet_50_1by2_nsfw.caffemodel ", caffe.TEST)
        self.caffe_transformer = caffe.io.Transformer({'data': nsfw_net.blobs['data'].data.shape})
        self.caffe_transformer.set_transpose('data', (2, 0, 1))  # move image channels to outermost
        self.caffe_transformer.set_mean('data', np.array([104, 117, 123]))  # subtract the dataset-mean value in each channel
        self.caffe_transformer.set_raw_scale('data', 255)  # rescale to [0, 255]
        self.caffe_transformer.set_channel_swap('data', (2, 1, 0))  # swap channels from RGB to BGR


app = Flask(__name__)


@app.route("/query", methods=["POST"])
def query():
    json_query = request.get_json()
    print json_query
    ret = [len(x) for x in json_query]
    return jsonify(ret)
