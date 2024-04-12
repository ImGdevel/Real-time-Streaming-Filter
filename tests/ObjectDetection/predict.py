from ultralytics import YOLO
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# Load a model
model = YOLO('yolov8n.pt')  # load an official model
model = YOLO('runs/detect/train32/weights/best.pt')  # load a custom model

# Validate the model

results = model('https://ultralytics.com/images/bus.jpg')  # predict on an image