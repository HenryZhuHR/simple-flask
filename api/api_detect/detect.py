import torch
from torch import Tensor
from torchvision import transforms,datasets
from PIL import Image
from .nss.MSCN import *
import numpy as np
from sklearn.externals import joblib

classes=('正常样本', '对抗样本')
class Detect:
    def __init__(self, model_path, device, image_tensor ,thre):
        self.model_path = model_path
        self.image_tensor:Tensor = image_tensor
        self.thre =thre

        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        # device = torch.device(device if torch.cuda.is_available() else 'cpu')

    def detect(self):
        ### Load Model and Parameters
        clf = joblib.load(self.model_path)
        img_ = self.image_tensor.unsqueeze(0)
        #culculate NSS value
        min_ = np.array([0.34282078, 0.05792056, 0.23479045, -0.21415752, 0.00968714, 0.01659025,
                         0.25033466, -0.22837449, 0.01565463, 0.00953424, 0.2598395, -0.22927241,
                         0.01340715, 0.00706881, 0.25834958, -0.23225086, 0.01603434, 0.00485092])
        max_ = np.array([1.48239649e+06, 7.87734764e-01, 1.71664076e+00, 2.00939974e-01,
                         6.80209686e-01, 4.41185997e-01, 1.72642714e+00, 2.18461737e-01,
                         7.02766262e-01, 4.26992011e-01, 1.67426405e+00, 1.25171493e-01,
                         6.33723661e-01, 5.08113247e-01, 1.66045004e+00, 9.20592683e-02,
                         6.36843824e-01, 5.04041197e-01])

        X = np.array([])
        img = img_.reshape(224, 224, 3)

        parameters = calculate_brisque_features(img)
        parameters = parameters.reshape((1, -1))
        X = parameters

        X = scale_features(X, min_, max_)

        #predict
        pred = clf.predict(X)
        prob = clf.predict_proba(X)
        ind =int(pred)
        pred_class = classes[ind]
        # print('该样本是一张：', pred_class)
        # print('对抗样本风险分数为：{:.2f}%'.format(100*prob[0][1]))
        if ind == 1 and prob[0][ind] >= self.thre:
            # print('This image is an adversarial example and will be discarded!')
            is_adversarialExample = 1
        else:
            is_adversarialExample = 0

        return is_adversarialExample,prob[0][1],self.thre


