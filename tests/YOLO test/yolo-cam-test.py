from ultralytics import YOLO

model = YOLO("models/yolov8n-oiv7.pt")

results = model.predict(source="0", show=True)