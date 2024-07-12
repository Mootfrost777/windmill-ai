from ultralytics import YOLO
from app.config import config
from app.models import Defect
from dataclasses import dataclass
import json


@dataclass
class CoordinatesStorage:
    x: int
    y: int
    w: int
    h: int


def load_model():
    global model
    model = YOLO(config.yolo_model_path)


def predict(image_paths):
    results = model.predict(image_paths, conf=0.7, iou=0.3, imgsz=320)
    res = []
    for result in results:
        boxes = result.boxes
        if boxes is None:
            res.append([])
            continue

        defects = []
        for box, conf, cls in zip(boxes.xyxy, boxes.conf, boxes.cls):
            defects.append(Defect(
                coordinates=json.dumps(CoordinatesStorage(*map(int, box)).__dict__),
                confidence=float(conf),
                type_id=int(cls)
            ))
        res.append(defects)
    return res


__all__ = ['load_model', 'predict']