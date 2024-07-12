import torch
from torchvision import models
from torchvision import transforms
from PIL import Image
import torch.nn as nn
from app.config import config
from os import path


def load_model():
    global model, device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = models.resnet50(pretrained=False)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 2)
    model.load_state_dict(torch.load(config.bin_model_path, map_location=torch.device('cpu')))
    model = model.to(device)
    model.eval()


classes = [True, False]
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


def predict(image_paths):
    images = [transform(Image.open(img).convert("RGB")) for img in image_paths]
    images = torch.stack(images)
    images = images.to(device)
    with torch.no_grad():
        outputs = model(images)
    _, predicted = torch.max(outputs, 1)
    items = [classes[pred.item()] for pred in predicted]
    return items


__all__ = ['load_model', 'predict']