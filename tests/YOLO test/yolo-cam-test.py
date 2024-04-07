from ultralytics import YOLO
from PIL import Image
import cv2

model = YOLO("models/yolov8n-oiv7.pt")

results = model.predict(source="0", show=True)