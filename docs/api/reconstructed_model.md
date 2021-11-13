
# 重建防御
将图片推理并且返回推理预测结果。在调用之前，需要先调用[选择图片](api/select_image.md)或者[上传图片](api/upload_image.md)
## 1.接口描述



接口地址：`/api/reconstructed_model`

请求方法：POST

## 2.输入参数

无输入，但确保在调用之前，已经[选择图片](api/select_image.md)或者[上传图片](api/upload_image.md)


## 3.输出参数

| 返回参数 | 描述                                                            |
| :------- | :-------------------------------------------------------------- |
| image    | 输入模型的图片的base64编码，不包含头部 `data:image/png;base64,` |
| Error    | 包含错误码`Code`和错误提示`Message`                             |

## 4.示例

**输入示例**
```curl
POST /api/reconstructed_model HTTP/1.1
Content-Type: application/json
```

**输出示例**
```json
{
    "image": <base_64_image>,
}
```

**错误返回实例**
```json
"Error": {
    "Code": "ReconstructedModel.ModelError",
    "Message": "error in load model"
}
```

## 5.错误码
| 错误码                     | 描述                       |
| :------------------------- | :------------------------- |
| ReconstructedModel.ModelError | 模型加载失败。             |
| ReconstructedModel.NotImage | 未选择或者未上传图片。             |

