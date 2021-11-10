import torch
from torchvision import transforms,datasets
from PIL import Image
from sklearn import svm
from nss.MSCN import *

from sklearn.externals import joblib#调用加载模型的API
from sklearn import preprocessing
# import joblib
from sklearn import svm #调用模型的API


classes=('正常样本', '对抗样本')
class Detect:
    def __init__(self, model, device, batch_size, image_in ,thre):
        """
        :param model:       Dir of recon_model.pt, e.g.
        :param device:      Cuda device, e.g. 'cuda:1'
        /data.jpg
        :param image_num:   The number of images, e.g. 1, 10 or 100
        :param image_in:    Input image or images
        :param thre:        the threshold of classification
        """
        self.model = model
        self.batch_size = batch_size
        self.image_in = image_in
        self.thre =thre

        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        # device = torch.device(device if torch.cuda.is_available() else 'cpu')

    def detect(self):
        ### Load Model and Parameters
        clf = joblib.load('Detect.pkl')

        ### Loading image data

        """
        Reading & Saving 1 picture
                 e.g. self.image_in = "/workspace/yjt/gc10_dsets/data.jpg"
        """
        img_path = self.image_in
        transform_data = transforms.ToTensor()
        img = Image.open(img_path)
        img_ = transform_data(img).unsqueeze(0)
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
        print('该样本是一张：', pred_class)
        print('对抗样本风险分数为：{:.2f}%'.format(100*prob[0][1]))
        if ind == 1 and prob[0][ind] >= self.thre:
            print('This image is an adversarial example and will be discarded!')
            flag = 1
        else:
            flag = 0

        return flag



def main():
    test = Detect(model='Detect.pkl', device='cuda:1', batch_size=1,
                 image_in="recon_101201.png", thre=0.8)
    test.detect()


if __name__ == '__main__':
    main()
