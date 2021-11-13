import time
from multiprocessing import Process
from PIL import Image
# from yolo_api.yolo import YOLO
from api.api_yolo.yolo import YOLO

import cv2
import numpy as np
import _thread
import time
np.set_printoptions(suppress=True)



def run_forever(net, capture):

    while 1:
        ref, frame = capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(np.uint8(frame))
        frame, conf = net.detect_image1(frame)
        frame = np.array(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imshow("video", frame)
        c = cv2.waitKey(1) & 0xff

        if c == ord('q'):
            capture.release()
            break

    capture.release()
    cv2.destroyAllWindows()


def main():
    net = YOLO(
        model_path='api/api_yolo/yolo.pth', 
        classes_path='api/api_yolo/classes.txt')
    capture = cv2.VideoCapture(0)
    p = Process(target=run_forever(net=net, capture=capture))


    p.start()
    print('start a process.')
    while 1:
        time.sleep(10)
        print('    ==Main')
        print("%s" % (time.ctime(time.time())))



if __name__ == '__main__':
    main()