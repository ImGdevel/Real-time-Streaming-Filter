from ultralytics import YOLO
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# Load a model
model = YOLO('model/yolov8n-oiv7.pt')  # load a pretrained model (recommended for training

# Train the model
if __name__ == '__main__':
    # results = model.train(data='coco.yaml', epochs=100, imgsz=640) 
    results = model.train(data='smoking/data.yaml', epochs=100, imgsz=640)