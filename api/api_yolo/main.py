from PIL import Image
from .yolo import YOLO

import cv2
import numpy as np
np.set_printoptions(suppress=True)

from torchvision import transforms

if __name__ == '__main__':

    path = "./img/001.jpg"
    image = Image.open(path)
    net = YOLO(model_path='api/api_yolo/yolo.pth',classes_path='api/api_yolo/classes.txt')
    r_image, conf = net.detect_image1(image)
    # r_image.show()
    print(conf)