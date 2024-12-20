import os

from ultralytics import YOLO

model = YOLO('D:\\PyProjects\\Open_A-YAY\\YOLOv8epoch20.pt')
model.predict(
    source=[
        'D:\\PyProjects\\Open_A-YAY\\image_processing\\images\\' + name
        for name in os.listdir('D:\\PyProjects\\Open_A-YAY\\image_processing\\images')
    ],
    save=True,
    show_labels=True,
    show_conf=True,
    name="images",
    conf=0.25,
    agnostic_nms=True,
)
