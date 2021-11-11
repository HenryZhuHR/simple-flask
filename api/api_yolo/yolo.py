import colorsys
import os
import time

import numpy as np

import torch
import torch.nn as nn
from PIL import ImageDraw, ImageFont
from PIL import Image

from .yolonet import YoloBody
from torchvision.ops import nms, boxes
# from utils.utils import cvtColor, preprocess_input, resize_image
# from utils.utils_bbox import decode_outputs, non_max_suppression

'''
训练自己的数据集必看注释！
'''


def get_classes(classes_path):
    with open(classes_path, encoding='utf-8') as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]
    return class_names, len(class_names)

def cvtColor(image):
    if len(np.shape(image)) == 3 and np.shape(image)[-2] == 3:
        return image
    else:
        image = image.convert('RGB')
        return image

def resize_image(image, size, letterbox_image):
    iw, ih  = image.size
    w, h    = size
    if letterbox_image:
        scale   = min(w/iw, h/ih)
        nw      = int(iw*scale)
        nh      = int(ih*scale)

        image   = image.resize((nw,nh), Image.BICUBIC)
        new_image = Image.new('RGB', size, (128,128,128))
        new_image.paste(image, ((w-nw)//2, (h-nh)//2))
    else:
        new_image = image.resize((w, h), Image.BICUBIC)
    return new_image

def preprocess_input(image):
    image /= 255.0
    image -= np.array([0.485, 0.456, 0.406])
    image /= np.array([0.229, 0.224, 0.225])
    return image

def yolo_correct_boxes(box_xy, box_wh, input_shape, image_shape, letterbox_image):
    #-----------------------------------------------------------------#
    #   把y轴放前面是因为方便预测框和图像的宽高进行相乘
    #-----------------------------------------------------------------#
    box_yx = box_xy[..., ::-1]
    box_hw = box_wh[..., ::-1]
    input_shape = np.array(input_shape)
    image_shape = np.array(image_shape)

    if letterbox_image:
        #-----------------------------------------------------------------#
        #   这里求出来的offset是图像有效区域相对于图像左上角的偏移情况
        #   new_shape指的是宽高缩放情况
        #-----------------------------------------------------------------#
        new_shape = np.round(image_shape * np.min(input_shape/image_shape))
        offset  = (input_shape - new_shape)/2./input_shape
        scale   = input_shape/new_shape

        box_yx  = (box_yx - offset) * scale
        box_hw *= scale

    box_mins    = box_yx - (box_hw / 2.)
    box_maxes   = box_yx + (box_hw / 2.)
    boxes  = np.concatenate([box_mins[..., 0:1], box_mins[..., 1:2], box_maxes[..., 0:1], box_maxes[..., 1:2]], axis=-1)
    boxes *= np.concatenate([image_shape, image_shape], axis=-1)
    return boxes

def decode_outputs(outputs, input_shape):
    grids   = []
    strides = []
    hw      = [x.shape[-2:] for x in outputs]
    outputs = torch.cat([x.flatten(start_dim=2) for x in outputs], dim=2).permute(0, 2, 1)
    outputs[:, :, 4:] = torch.sigmoid(outputs[:, :, 4:])
    for h, w in hw:
        #---------------------------#
        #   根据特征层生成网格点
        #---------------------------#
        grid_y, grid_x  = torch.meshgrid([torch.arange(h), torch.arange(w)])
        grid            = torch.stack((grid_x, grid_y), 2).view(1, -1, 2)
        shape           = grid.shape[:2]

        grids.append(grid)
        strides.append(torch.full((shape[0], shape[1], 1), input_shape[0] / h))
    #---------------------------#
    #   将网格点堆叠到一起
    #---------------------------#
    grids               = torch.cat(grids, dim=1).type(outputs.type())
    strides             = torch.cat(strides, dim=1).type(outputs.type())
    #------------------------#
    #   根据网格点进行解码
    #------------------------#
    outputs[..., :2]    = (outputs[..., :2] + grids) * strides
    outputs[..., 2:4]   = torch.exp(outputs[..., 2:4]) * strides
    #-----------------#
    #   归一化
    #-----------------#
    outputs[..., [0,2]] = outputs[..., [0,2]] / input_shape[1]
    outputs[..., [1,3]] = outputs[..., [1,3]] / input_shape[0]
    return outputs


# def non_max_suppression(prediction, num_classes, input_shape, image_shape, letterbox_image, conf_thres=0.5,
#                         nms_thres=0.4):
#     # ----------------------------------------------------------#
#     #   将预测结果的格式转换成左上角右下角的格式。
#     #   prediction  [batch_size, num_anchors, 85]
#     # ----------------------------------------------------------#
#     box_corner = prediction.new(prediction.shape)
#     box_corner[:, :, 0] = prediction[:, :, 0] - prediction[:, :, 2] / 2
#     box_corner[:, :, 1] = prediction[:, :, 1] - prediction[:, :, 3] / 2
#     box_corner[:, :, 2] = prediction[:, :, 0] + prediction[:, :, 2] / 2
#     box_corner[:, :, 3] = prediction[:, :, 1] + prediction[:, :, 3] / 2
#     prediction[:, :, :4] = box_corner[:, :, :4]
#
#     output = [None for _ in range(len(prediction))]
#     for i, image_pred in enumerate(prediction):
#         # ----------------------------------------------------------#
#         #   对种类预测部分取max。
#         #   class_conf  [num_anchors, 1]    种类置信度
#         #   class_pred  [num_anchors, 1]    种类
#         # ----------------------------------------------------------#
#         class_conf, class_pred = torch.max(image_pred[:, 5:5 + num_classes], 1, keepdim=True)
#
#         # ----------------------------------------------------------#
#         #   利用置信度进行第一轮筛选
#         # ----------------------------------------------------------#
#         conf_mask = (image_pred[:, 4] * class_conf[:, 0] >= conf_thres).squeeze()
#
#         if not image_pred.size(0):
#             continue
#         # -------------------------------------------------------------------------#
#         #   detections  [num_anchors, 7]
#         #   7的内容为：x1, y1, x2, y2, obj_conf, class_conf, class_pred
#         # -------------------------------------------------------------------------#
#         detections = torch.cat((image_pred[:, :5], class_conf, class_pred.float()), 1)
#         detections = detections[conf_mask]
#
#         nms_out_index = boxes.batched_nms(
#             detections[:, :4],
#             detections[:, 4] * detections[:, 5],
#             detections[:, 6],
#             nms_thres,
#         )
#
#         output[i] = detections[nms_out_index]
#
#         if output[i] is not None:
#             output[i] = output[i].cpu().numpy()
#             box_xy, box_wh = (output[i][:, 0:2] + output[i][:, 2:4]) / 2, output[i][:, 2:4] - output[i][:, 0:2]
#             output[i][:, :4] = yolo_correct_boxes(box_xy, box_wh, input_shape, image_shape, letterbox_image)
#
#     return output

def non_max_suppression(prediction, num_classes, input_shape, image_shape, letterbox_image, conf_thres=0.5,
                        nms_thres=0.4):
    # ----------------------------------------------------------#
    #   将预测结果的格式转换成左上角右下角的格式。
    #   prediction  [batch_size, num_anchors, 85]
    # ----------------------------------------------------------#
    box_corner = prediction.new(prediction.shape)
    box_corner[:, :, 0] = prediction[:, :, 0] - prediction[:, :, 2] / 2
    box_corner[:, :, 1] = prediction[:, :, 1] - prediction[:, :, 3] / 2
    box_corner[:, :, 2] = prediction[:, :, 0] + prediction[:, :, 2] / 2
    box_corner[:, :, 3] = prediction[:, :, 1] + prediction[:, :, 3] / 2
    prediction[:, :, :4] = box_corner[:, :, :4]

    output = [None for _ in range(len(prediction))]
    output_all = [None for _ in range(len(prediction))]
    for i, image_pred in enumerate(prediction):
        # ----------------------------------------------------------#
        #   对种类预测部分取max。
        #   class_conf  [num_anchors, 1]    种类置信度
        #   class_pred  [num_anchors, 1]    种类
        # ----------------------------------------------------------#
        class_conf, class_pred = torch.max(image_pred[:, 5:5 + num_classes], 1, keepdim=True)
        class_all = image_pred[:, 5:5 + num_classes]
        # class_all = nn.Softmax(dim=1)(image_pred[:, 5:5 + num_classes])

        # ----------------------------------------------------------#
        #   利用置信度进行第一轮筛选
        # ----------------------------------------------------------#
        conf_mask = (image_pred[:, 4] * class_conf[:, 0] >= conf_thres).squeeze()

        if not image_pred.size(0):
            continue
        # -------------------------------------------------------------------------#
        #   detections  [num_anchors, 7]
        #   7的内容为：x1, y1, x2, y2, obj_conf, class_conf, class_pred
        # -------------------------------------------------------------------------#
        detections = torch.cat((image_pred[:, :5], class_conf, class_pred.float()), 1)
        detections = detections[conf_mask]

        detections_all = torch.cat((image_pred[:, :5], class_all, class_pred.float()), 1)
        detections_all = detections_all[conf_mask]

        nms_out_index = boxes.batched_nms(
            detections[:, :4],
            detections[:, 4] * detections[:, 5],
            detections[:, 6],
            nms_thres,
        )

        output[i] = detections[nms_out_index]
        output_all[i] = detections_all[nms_out_index]


        if output[i] is not None:
            output[i] = output[i].cpu().numpy()
            box_xy, box_wh = (output[i][:, 0:2] + output[i][:, 2:4]) / 2, output[i][:, 2:4] - output[i][:, 0:2]
            output[i][:, :4] = yolo_correct_boxes(box_xy, box_wh, input_shape, image_shape, letterbox_image)

            # print(output_all[i][:, 5: 5 + num_classes])
            output_all[i][:, 5: 5 + num_classes] = output_all[i][:, 5: 5 + num_classes] * output_all[i][:, 4].reshape((-1, 1))

            output_all[i] = output_all[i].cpu().numpy()
            output_all[i][:, :4] = yolo_correct_boxes(box_xy, box_wh, input_shape, image_shape, letterbox_image)


    return output, output_all



class YOLO(object):
    _defaults = {
        #--------------------------------------------------------------------------#
        #   使用自己训练好的模型进行预测一定要修改model_path和classes_path！
        #   model_path指向logs文件夹下的权值文件，classes_path指向model_data下的txt
        #   如果出现shape不匹配，同时要注意训练时的model_path和classes_path参数的修改
        #--------------------------------------------------------------------------#
        "model_path"        : None,
        "classes_path"      : None,
        #---------------------------------------------------------------------#
        #   输入图片的大小，必须为32的倍数。
        #---------------------------------------------------------------------#
        "input_shape"       : [512, 512],
        #---------------------------------------------------------------------#
        #   所使用的YoloX的版本。s、m、l、x
        #---------------------------------------------------------------------#
        "phi"               : 's',
        #---------------------------------------------------------------------#
        #   只有得分大于置信度的预测框会被保留下来
        #---------------------------------------------------------------------#
        "confidence"        : 0.5,
        #---------------------------------------------------------------------#
        #   非极大抑制所用到的nms_iou大小
        #---------------------------------------------------------------------#
        "nms_iou"           : 0.3,
        #---------------------------------------------------------------------#
        #   该变量用于控制是否使用letterbox_image对输入图像进行不失真的resize，
        #   在多次测试后，发现关闭letterbox_image直接resize的效果更好
        #---------------------------------------------------------------------#
        "letterbox_image"   : False,
        #-------------------------------#
        #   是否使用Cuda
        #   没有GPU可以设置成False
        #-------------------------------#
        "cuda"              : False,
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    #---------------------------------------------------#
    #   初始化YOLO
    #---------------------------------------------------#
    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        for name, value in kwargs.items():
            setattr(self, name, value)
            
        #---------------------------------------------------#
        #   获得种类和先验框的数量
        #---------------------------------------------------#
        self.class_names, self.num_classes  = get_classes(self.classes_path)

        #---------------------------------------------------#
        #   画框设置不同的颜色
        #---------------------------------------------------#
        hsv_tuples = [(x / self.num_classes, 1., 1.) for x in range(self.num_classes)]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), self.colors))
        self.generate()

    #---------------------------------------------------#
    #   生成模型
    #---------------------------------------------------#
    def generate(self):
        self.net    = YoloBody(self.num_classes, self.phi)
        device      = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.net.load_state_dict(torch.load(self.model_path, map_location=device))
        self.net    = self.net.eval()

        print('{} model, and classes loaded.'.format(self.model_path))

        if self.cuda:
            self.net = nn.DataParallel(self.net)
            self.net = self.net.cuda()

    #---------------------------------------------------#
    #   检测图片
    #---------------------------------------------------#
    def detect_image(self, image):
        image_shape = np.array(np.shape(image)[0:2])

        #---------------------------------------------------------#
        #   在这里将图像转换成RGB图像，防止灰度图在预测时报错。
        #   代码仅仅支持RGB图像的预测，所有其它类型的图像都会转化成RGB
        #---------------------------------------------------------#
        image       = cvtColor(image)
        #---------------------------------------------------------#
        #   给图像增加灰条，实现不失真的resize
        #   也可以直接resize进行识别
        #---------------------------------------------------------#
        image_data  = resize_image(image, (self.input_shape[1],self.input_shape[0]), self.letterbox_image)
        #---------------------------------------------------------#
        #   添加上batch_size维度
        #---------------------------------------------------------#
        image_data  = np.expand_dims(np.transpose(preprocess_input(np.array(image_data, dtype='float32')), (2, 0, 1)), 0)




        with torch.no_grad():
            images = torch.from_numpy(image_data)
            if self.cuda:
                images = images.cuda()
            #---------------------------------------------------------#
            #   将图像输入网络当中进行预测！
            #---------------------------------------------------------#
            outputs = self.net(images)
            outputs = decode_outputs(outputs, self.input_shape)
            #---------------------------------------------------------#
            #   将预测框进行堆叠，然后进行非极大抑制
            #---------------------------------------------------------#
            results = non_max_suppression(outputs, self.num_classes, self.input_shape, 
                        image_shape, self.letterbox_image, conf_thres = self.confidence, nms_thres = self.nms_iou)

            position = np.array([0, 0, image.size[0], image.size[1]])
                                                    
            if results[0].shape[0] ==0:
                return position

            top_label   = np.array(results[0][:, 6], dtype = 'int32')
            top_conf    = results[0][:, 4] * results[0][:, 5]
            top_boxes   = results[0][:, :4]


        s = 0
        max_score = 0
        for i, c in list(enumerate(top_label)):
            predicted_class = self.class_names[int(c)]
            box             = top_boxes[i]
            score = top_conf[i]

            top, left, bottom, right = box

            top     = max(0, np.floor(top).astype('int32'))
            left    = max(0, np.floor(left).astype('int32'))
            bottom  = min(image.size[1], np.floor(bottom).astype('int32'))
            right   = min(image.size[0], np.floor(right).astype('int32'))

            label = '{} {:.2f}'.format(predicted_class, score)
            print(label, top, left, bottom, right)

            # 返回面积最大的框的位置
            if (bottom - top) * (right - left) > s:
                s = (bottom - top) * (right - left)
                position = np.array([left, top, right, bottom])

            # 返回置信度最高的框的位置
            # if score > max_score:
            #     max_score = score
            #     position = np.array([left, top, right, bottom])


        return position

    def detect_image1(self, image):
        image_shape = np.array(np.shape(image)[0:2])
        # ---------------------------------------------------------#
        #   在这里将图像转换成RGB图像，防止灰度图在预测时报错。
        #   代码仅仅支持RGB图像的预测，所有其它类型的图像都会转化成RGB
        # ---------------------------------------------------------#
        image = cvtColor(image)
        # ---------------------------------------------------------#
        #   给图像增加灰条，实现不失真的resize
        #   也可以直接resize进行识别
        # ---------------------------------------------------------#
        image_data = resize_image(image, (self.input_shape[1], self.input_shape[0]), self.letterbox_image)
        # ---------------------------------------------------------#
        #   添加上batch_size维度
        # ---------------------------------------------------------#
        image_data = np.expand_dims(np.transpose(preprocess_input(np.array(image_data, dtype='float32')), (2, 0, 1)), 0)

        with torch.no_grad():
            images = torch.from_numpy(image_data)
            if self.cuda:
                images = images.cuda()
            # ---------------------------------------------------------#
            #   将图像输入网络当中进行预测！
            # ---------------------------------------------------------#
            outputs = self.net(images)
            outputs = decode_outputs(outputs, self.input_shape)
            # ---------------------------------------------------------#
            #   将预测框进行堆叠，然后进行非极大抑制
            # ---------------------------------------------------------#
            results, results_all = non_max_suppression(outputs, self.num_classes, self.input_shape,
                                          image_shape, self.letterbox_image, conf_thres=self.confidence,
                                          nms_thres=self.nms_iou)

            if results[0].shape[0] ==0:

                return image, np.array([0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1],dtype='float32')

            top_label = np.array(results[0][:, 6], dtype='int32')
            top_conf = results[0][:, 4] * results[0][:, 5]
            top_boxes = results[0][:, :4]

            # top_conf_all = np.multiply(results_all[0][:, 5:15], results[0][:, 4, np.newaxis])
            top_conf_all = results_all[0][:, 5:15]

        # ---------------------------------------------------------#
        #   设置字体与边框厚度
        # ---------------------------------------------------------#
        # font = ImageFont.truetype(font='model_data/simhei.ttf',size=np.floor(6e-2 * image.size[1] + 0.5).astype('int32'))
        thickness = int(3 * max((image.size[0] + image.size[1]) // np.mean(self.input_shape), 1))

        # ---------------------------------------------------------#
        #   图像绘制
        # ---------------------------------------------------------#

        s = 0
        index = 0
        for i, c in list(enumerate(top_label)):
            box = top_boxes[i]
            top, left, bottom, right = box

            top = max(0, np.floor(top).astype('int32'))
            left = max(0, np.floor(left).astype('int32'))
            bottom = min(image.size[1], np.floor(bottom).astype('int32'))
            right = min(image.size[0], np.floor(right).astype('int32'))

            # 返回面积最大的框的位置
            if (bottom - top) * (right - left) > s:
                s = (bottom - top) * (right - left)
                index = i

        box = top_boxes[index]
        top, left, bottom, right = box
        top = max(0, np.floor(top).astype('int32'))
        left = max(0, np.floor(left).astype('int32'))
        bottom = min(image.size[1], np.floor(bottom).astype('int32'))
        right = min(image.size[0], np.floor(right).astype('int32'))
        draw = ImageDraw.Draw(image)
        for i in range(thickness):
            draw.rectangle([left + i, top + i, right - i, bottom - i], outline=self.colors[c])
        del draw

        ten_conf = top_conf_all[index]
        max_conf = ten_conf[top_label[index]]
        ten_conf = (1 - max_conf) * ten_conf / (ten_conf.sum() - max_conf)
        ten_conf[top_label[index]] = max_conf




        # for i, c in list(enumerate(top_label)):
        #     predicted_class = self.class_names[int(c)]
        #     box = top_boxes[i]
        #     score = top_conf[i]
        #
        #     top, left, bottom, right = box
        #
        #     top = max(0, np.floor(top).astype('int32'))
        #     left = max(0, np.floor(left).astype('int32'))
        #     bottom = min(image.size[1], np.floor(bottom).astype('int32'))
        #     right = min(image.size[0], np.floor(right).astype('int32'))
        #
        #     label = '{} {:.2f}'.format(predicted_class, score)
        #     draw = ImageDraw.Draw(image)
        #     label_size = draw.textsize(label, font)
        #     label = label.encode('utf-8')
        #     # print(label, top, left, bottom, right)
        #
        #     if top - label_size[1] >= 0:
        #         text_origin = np.array([left, top - label_size[1]])
        #     else:
        #         text_origin = np.array([left, top + 1])
        #
        #     for i in range(thickness):
        #         draw.rectangle([left + i, top + i, right - i, bottom - i], outline=self.colors[c])
        #     # draw.rectangle([tuple(text_origin), tuple(text_origin + label_size)], fill=self.colors[c])
        #     # draw.text(text_origin, str(label, 'UTF-8'), fill=(0, 0, 0), font=font)
        #     del draw

        return image, ten_conf



