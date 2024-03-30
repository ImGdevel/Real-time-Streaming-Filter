from ultralytics import YOLO
import multiprocessing
from multiprocessing import freeze_support

def main():
    # Load a model
    model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
    
    # Use the model
    model.train(data="coco128.yaml", epochs=3)  # train the model
    metrics = model.val()  # evaluate model performance on the validation set
    results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
    path = model.export(format="onnx")  # export the model to ONNX format

if __name__ == '__main__':
    freeze_support()
    multiprocessing.set_start_method('spawn')  # Set start method to 'spawn'
    main()
