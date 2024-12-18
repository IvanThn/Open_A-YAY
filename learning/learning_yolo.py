from ultralytics import YOLO

model = YOLO('D:\\PyProjects\\Open_A-YAY\\runs\\detect\\YOLOv8s17\\weights\\last.pt')


def start_learning():
    return model.train(
        data='D:/content/trafic_signs.yaml',  # imgsz=1280
        epochs=15,
        batch=16,  # 6
        device=0,
        name='YOLOv8s',
        resume=True,
    )


if __name__ == '__main__':
    start_learning()
