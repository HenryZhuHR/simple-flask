
# 对抗样本检测
将图片推理并且返回推理预测结果。在调用之前，需要先调用[选择图片](api/select_image.md)或者[上传图片](api/upload_image.md)
## 1.接口描述



接口地址：`/api/adversarial_detect`

请求方法：POST

## 2.输入参数

在调用之前，已经[选择图片](api/select_image.md)或者[上传图片](api/upload_image.md)
| 输入参数 | 描述                                                                                               |
| :------- | :------------------------------------------------------------------------------------------------- |
| mode     | `mode` 取 `original_image` 模型对原始图像进行预测，取 `reconstructed_image` 模型对重建图像进行预测 |


## 3.输出参数

| 返回参数              | 描述                                                                               |
| :-------------------- | :--------------------------------------------------------------------------------- |
| is_adversarialExample | 图片是否为对抗样本，`0`表示正常样本，`1`表示对抗样本                               |
| probability           | 图片是否为对抗样本的概率                                                           |
| threshold             | 判断是否为对抗样本的阈值，当概率`probability`大于阈值`threshold`时，判定为对抗样本 |
| Error                 | 包含错误码`Code`和错误提示`Message`                                                |

## 4.示例

**输入示例**
```curl
POST /api/adversarial_detect HTTP/1.1
Content-Type: application/json

{
    "mode": "original_image",
}
```

**输出示例**
```json
{
    "is_adversarialExample": 0,
    "probability": 0.0024473629997639797,
    "threshold": 0.8
}
```

**错误返回实例**
```json
"Error": {
    "Code": "AdversarialDetect.NotImage",
    "Message": "not select or upload image"
}
```

## 5.错误码
| 错误码               | 描述                 |
| :------------------- | :------------------- |
| AdversarialDetect.LossParameter | 缺少参数 `mode`             |
| AdversarialDetect.NotImage | 未选择或者未上传图片 |

