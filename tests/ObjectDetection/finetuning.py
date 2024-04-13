import fiftyone as fo
import fiftyone.zoo as foz
from fiftyone import ViewField as F
import numpy as np
import os
from tqdm import tqdm
from ultralytics import YOLO

import fiftyone.utils.random as four

detection_model = YOLO("yolov8n.pt")
seg_model = YOLO("yolov8n-seg.pt")

results = detection_model("https://ultralytics.com/images/bus.jpg")

dataset = foz.load_zoo_dataset(
    'coco-2017',
    split='validation',
)

coco_classes = [c for c in dataset.default_classes if not c.isnumeric()]

def export_yolo_data(
    samples,
    export_dir,
    classes,
    label_field = "ground_truth",
    split = None
    ):

    if type(split) == list:
        splits = split
        for split in splits:
            export_yolo_data(
                samples,
                export_dir,
                classes,
                label_field,
                split
            )
    else:
        if split is None:
            split_view = samples
            split = "val"
        else:
            split_view = samples.match_tags(split)

        split_view.export(
            export_dir=export_dir,
            dataset_type=fo.types.YOLOv5Dataset,
            label_field=label_field,
            classes=classes,
            split=split
        )
        
coco_val_dir = "coco_val"
export_yolo_data(dataset, coco_val_dir, coco_classes)

# label_file = "runs/detect/predict/labels/000000000139.txt"

# with open(label_file) as f:
#     print(f.read())
    
    
def read_yolo_detections_file(filepath):
    detections = []
    if not os.path.exists(filepath):
        return np.array([])

    with open(filepath) as f:
        lines = [line.rstrip('\n').split(' ') for line in f]

    for line in lines:
        detection = [float(l) for l in line]
        detections.append(detection)
    return np.array(detections)


def _uncenter_boxes(boxes):
    '''convert from center coords to corner coords'''
    boxes[:, 0] -= boxes[:, 2]/2.
    boxes[:, 1] -= boxes[:, 3]/2.
    
def _get_class_labels(predicted_classes, class_list):
    labels = (predicted_classes).astype(int)
    labels = [class_list[l] for l in labels]
    return labels

def convert_yolo_detections_to_fiftyone(
    yolo_detections,
    class_list
    ):

    detections = []
    if yolo_detections.size == 0:
        return fo.Detections(detections=detections)

    boxes = yolo_detections[:, 1:-1]
    _uncenter_boxes(boxes)

    confs = yolo_detections[:, -1]
    labels = _get_class_labels(yolo_detections[:, 0], class_list)

    for label, conf, box in zip(labels, confs, boxes):
        detections.append(
            fo.Detection(
                label=label,
                bounding_box=box.tolist(),
                confidence=conf
            )
        )

    return fo.Detections(detections=detections)

def get_prediction_filepath(filepath, run_number = 1):
    run_num_string = ""
    if run_number != 1:
        run_num_string = str(run_number)
    filename = filepath.split("/")[-1].split(".")[0]
    return f"runs/detect/predict{run_num_string}/labels/{filename}.txt"

def add_yolo_detections(
    samples,
    prediction_field,
    prediction_filepath,
    class_list
    ):

    prediction_filepaths = samples.values(prediction_filepath)
    yolo_detections = [read_yolo_detections_file(pf) for pf in prediction_filepaths]
    detections =  [convert_yolo_detections_to_fiftyone(yd, class_list) for yd in yolo_detections]
    samples.set_values(prediction_field, detections)
    
filepaths = dataset.values("filepath")
prediction_filepaths = [get_prediction_filepath(fp) for fp in filepaths]
dataset.set_values(
    "yolov8n_det_filepath",
    prediction_filepaths
)

add_yolo_detections(
    dataset,
    "yolov8n",
    "yolov8n_det_filepath",
    coco_classes
)

session = fo.launch_app(dataset)


def convert_yolo_segmentations_to_fiftyone(
    yolo_segmentations,
    class_list
    ):

    detections = []
    boxes = yolo_segmentations.boxes.xywhn
    if not boxes.shape or yolo_segmentations.masks is None:
        return fo.Detections(detections=detections)

    _uncenter_boxes(boxes)
    masks = yolo_segmentations.masks.masks
    labels = _get_class_labels(yolo_segmentations.boxes.cls, class_list)

    for label, box, mask in zip(labels, boxes, masks):
        ## convert to absolute indices to index mask
        w, h = mask.shape
        tmp =  np.copy(box)
        tmp[2] += tmp[0]
        tmp[3] += tmp[1]
        tmp[0] *= h
        tmp[2] *= h
        tmp[1] *= w
        tmp[3] *= w
        tmp = [int(b) for b in tmp]
        y0, x0, y1, x1 = tmp
        sub_mask = mask[x0:x1, y0:y1]

        detections.append(
            fo.Detection(
                label=label,
                bounding_box = list(box),
                mask = sub_mask.astype(bool)
            )
        )

    return fo.Detections(detections=detections)


# session = fo.launch_app(dataset)

detection_results = dataset.evaluate_detections(
    "yolov8n",
    eval_key="eval",
    compute_mAP=True,
    gt_field="ground_truth",
)

mAP = detection_results.mAP()
print(f"mAP = {mAP}")

counts = dataset.count_values("ground_truth.detections.label")

top20_classes = sorted(
    counts,
    key=counts.get,
    reverse=True
)[:20]

detection_results.print_report(classes=top20_classes)

test_dataset = dataset.filter_labels(
    "ground_truth",
    F("label") == "bird"
).filter_labels(
    "yolov8n",
    F("label") == "bird",
    only_matches=False
).clone()

test_dataset.name = "birds-test-dataset"
test_dataset.persistent = True

## set classes to just include birds
classes = ["bird"]

# session = fo.launch_app(dataset)


base_bird_results = test_dataset.evaluate_detections(
    "yolov8n",
    eval_key="base",
    compute_mAP=True,
)

mAP = base_bird_results.mAP()
print(f"Base mAP = {mAP}")

base_bird_results.print_report(classes=classes)


export_yolo_data(
    test_dataset,
    "birds_test",
    classes
)

train_dataset = foz.load_zoo_dataset(
    'coco-2017',
    split='train',
    classes=classes
).clone()

train_dataset.name = "birds-train-data"
train_dataset.persistent = True
train_dataset.save()

oi_samples = foz.load_zoo_dataset(
    "open-images-v6",
    classes = ["Bird"],
    only_matching=True,
    label_types="detections"
).map_labels(
    "ground_truth",
    {"Bird":"bird"}
)

train_dataset.merge_samples(oi_samples)


## delete existing tags to start fresh
train_dataset.untag_samples(train_dataset.distinct("tags"))

## split into train and val
four.random_split(
    train_dataset,
    {"train": 0.8, "val": 0.2}
)

## export in YOLO format
export_yolo_data(
    train_dataset,
    "birds_train",
    classes,
    split = ["train", "val"]
)

filepaths = test_dataset.values("filepath")
prediction_filepaths = [get_prediction_filepath(fp, run_number=2) for fp in filepaths]

test_dataset.set_values(
    "yolov8n_bird_det_filepath",
    prediction_filepaths
)

add_yolo_detections(
    birds_test_dataset,
    "yolov8n_bird",
    "yolov8n_bird_det_filepath",
    classes
)

# session = fo.launch_app(test_dataset)

finetune_bird_results = test_dataset.evaluate_detections(
    "yolov8n_bird",
    eval_key="finetune",
    compute_mAP=True,
)
print("yolov8n mAP: {}.format(base_bird_results.mAP())")
print("fine-tuned mAP: {}.format(finetune_bird_results.mAP())")

finetune_bird_results.print_report()

fn_view = dataset.sort_by("eval_fn", reverse=True)
session.view = fn_view

fp_view = dataset.sort_by("eval_fp", reverse=True)
session.view = fp_view
