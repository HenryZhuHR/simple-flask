
# 鲁棒模型
将图片推理并且返回推理预测结果
## 1.接口描述



接口地址：`/robust_model`

请求方法：POST

## 2.输入参数

| 请求参数  | 必选 | 类型   | 描述                   |
| :-------- | :--- | :----- | :--------------------- |
| file_name | 否   | String | 需要选择推理的图片文件，否则会使用上一次选择的图片或者初始默认的图片 |


## 3.输出参数

| 返回参数 | 描述                                |
| :------- | :---------------------------------- |
| image    | 输入模型的图片的base64编码                     |
| predict  | 预测的10个结果                      |
| Error    | 包含错误码`Code`和错误提示`Message` |

## 4.示例

**输入示例**
```curl
{
    "file_name":"./image.jpg"
}
```

**输出示例**
```json
{
    'image':<base_64_image_encode>,
    'predict': {
        'airplane': 0.0075752311386168,
        'automobile': 0.005625816062092781,
        'cargo_ship': 0.18090113997459412,
        'castle': 0.008153322152793407,
        'cg_ddg': 0.004138512071222067,
        'char': 0.009182588197290897,
        'cruise_ship': 0.0043475632555782795,
        'cvn': 0.007167038507759571,
        'monitor': 0.01417673658579588,
        'tanker_ship': 0.75873202085495
    }
}
```

**错误返回实例**
```json
'Error': {
    'Code': 'SelectImage.FileNotFound',
    'Message': 'request image file adv_101802.png not found'
}
```

## 5.错误码
| 错误码                            | 描述         |
| :-------------------------------- | :----------- |
| SelectImage.InvalidParameterValue | 参数值错误。 |
| RobustModel.FileNotFound          | 模型加载失败 |


