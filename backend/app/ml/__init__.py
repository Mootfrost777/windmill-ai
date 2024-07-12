from app.ml.binary import load_model as load_bin_model, predict as bin_predict
from app.ml.yolo import load_model as load_yolo_model, predict as yolo_predict


def load_models():
    load_bin_model()
    load_yolo_model()
