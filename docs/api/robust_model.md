
# 鲁棒模型
将图片推理并且返回推理预测结果。在调用之前，需要先调用[选择图片](api/select_image.md)或者[上传图片](api/upload_image.md)
## 1.接口描述



接口地址：`/robust_model`

请求方法：POST

## 2.输入参数

无输入，但确保在调用之前，已经[选择图片](api/select_image.md)或者[上传图片](api/upload_image.md)


## 3.输出参数

| 返回参数 | 描述                                |
| :------- | :---------------------------------- |
| image    | 输入模型的图片的base64编码          |
| predict  | 预测的10个结果                      |
| Error    | 包含错误码`Code`和错误提示`Message` |

## 4.示例

**输入示例**
```curl
POST /robust_model HTTP/1.1
Content-Type: application/json
```

**输出示例**
```json
{
    "image": <base_64_image>,
    "predict": {
        "airplane": 0.0075752311386168,
        "automobile": 0.005625816062092781,
        "cargo_ship": 0.18090113997459412,
        "castle": 0.008153322152793407,
        "cg_ddg": 0.004138512071222067,
        "char": 0.009182588197290897,
        "cruise_ship": 0.0043475632555782795,
        "cvn": 0.007167038507759571,
        "monitor": 0.01417673658579588,
        "tanker_ship": 0.75873202085495
    }
}
```

**字段说明**

| 字段                     | 名称                       |
| :----------------------- | :------------------------- |
| airplane                 | 飞机                       |
| automobile               | 汽车                       |
| cargo_ship               | 货船                       |
| castle                   | 城堡                       |
| cg_ddg                   | 战舰                       |
| char                     | 椅子                       |
| cruise_ship              | 游轮                       |
| cvn                      | 航母                       |
| monitor                  | 屏幕                       |
| tanker_ship              | 油船                       |



**错误返回实例**
```json
"Error": {
    "Code": "SelectImage.FileNotFound",
    "Message": "request image file adv_101802.png not found"
}
```

## 5.错误码
| 错误码                   | 描述                       |
| :----------------------- | :------------------------- |
| NotParameterGet          | 参数值错误或未获取参数值。 |
| RobustModel.FileNotFound | 模型加载失败。             |


