import os

from ultralytics import YOLO

model = YOLO('D:\\PyProjects\\Open_A-YAY\\best.pt')
model.predict(
    source=[
        'D:\\PyProjects\\Open_A-YAY\\image_processing\\images\\' + name
        for name in os.listdir('D:\\PyProjects\\Open_A-YAY\\image_processing\\images')
    ],
    save=True,
    show_labels=True,
    show_conf=True,
    name="images",
    conf=0.35,
    agnostic_nms=True,
)
