# API 文档

- [API 文档](#api-文档)
- [服务器地址](#服务器地址)
- [API 文档](#api-文档-1)
  - [选择图片](#选择图片)
  - [鲁棒模型](#鲁棒模型)
- [Browser 选择图像](#browser-选择图像)
- [Server 选择图像](#server-选择图像)
- [Browser 选择原始模型](#browser-选择原始模型)
- [Server 选择原始模型](#server-选择原始模型)
- [Browser 选择鲁棒模型](#browser-选择鲁棒模型)
- [Server 选择鲁棒模型](#server-选择鲁棒模型)
- [Browser 重建防御](#browser-重建防御)
- [Server 重建防御](#server-重建防御)
- [Browser 对抗检测](#browser-对抗检测)
- [Server 对抗检测](#server-对抗检测)
- [Browser 全防御流程](#browser-全防御流程)
- [Server 全防御流程](#server-全防御流程)
- [Browser 物理世界平台](#browser-物理世界平台)
- [Server 物理世界平台](#server-物理世界平台)

# 服务器地址
`http://1.116.121.100`

# API 文档
## 选择图片
**1.接口描述**

接口地址：`/select_image`

请求方法：POST

**2.输入参数**

| 请求参数  | 必选 | 类型   | 描述                       |
| :-------- | :--- | :----- | :------------------------- |
| file_name | 是   | String | 需要选择服务器上的图片文件 |

**3.输出参数**
| 返回参数 | 描述                                |
| :------- | :---------------------------------- |
| image    | 经过base64编码的图片数据            |
| Error    | 包含错误码`Code`和错误提示`Message` |

**4.示例**

**输入示例**
```curl
{
    "file_name":"./image.jpg"
}
```

**输出示例**
```json
{
    "image":<base_64_image_encode>
}
```

错误返回实例
```json
'Error': {
    'Code': 'SelectImage.FileNotFound',
    'Message': 'request image file adv_101802.png not found'
}
```

**5.错误码**
| 错误码                            | 描述             |
| :-------------------------------- | :--------------- |
| SelectImage.InvalidParameterValue | 参数值错误。     |
| SelectImage.FileNotFound          | 没有此图片文件。 |



## 鲁棒模型
**1.接口描述**

将图片推理并且返回推理预测结果

接口地址：`/robust_model`

请求方法：POST

**2.输入参数**

| 请求参数  | 必选 | 类型   | 描述                   |
| :-------- | :--- | :----- | :--------------------- |
| file_name | 否   | String | 需要选择推理的图片文件，否则会使用上一次选择的图片或者初始默认的图片 |


**3.输出参数**
| 返回参数 | 描述                                |
| :------- | :---------------------------------- |
| image    | 输入模型的图片的base64编码                     |
| predict  | 预测的10个结果                      |
| Error    | 包含错误码`Code`和错误提示`Message` |

**4.示例**

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

错误返回实例
```json
'Error': {
    'Code': 'SelectImage.FileNotFound',
    'Message': 'request image file adv_101802.png not found'
}
```

**5.错误码**
| 错误码                            | 描述         |
| :-------------------------------- | :----------- |
| SelectImage.InvalidParameterValue | 参数值错误。 |
| RobustModel.FileNotFound          | 模型加载失败 |
















































# Browser 选择图像

POST 请求

```json
{
  "command": "chooseImage",
  "image_name": "/**/image.jpg"
}
```

|    key     |   value    |
| :--------: | :--------: |
|  command   | 合法无报错 |
| image_name | 图片不合法 |

# Server 选择图像

```json
{
  "command": "chooseImage",
  "statement": 10,
  "imageOrigin": "imageOrigin"
}
```

- 返回值

| code  | chooseError1 |
| :---: | :----------: |
|  10   |  合法无报错  |
|  11   |  图片不合法  |

|     code     | imageOrigin |
| :----------: | :---------: |
| 返回原始图像 |

# Browser 选择原始模型

```json
{
  "command": "originModel"
}
```

# Server 选择原始模型

```json
{
  "command": "originModel",
  "chooseError2": 20,
  "imageNumber1": 1,
  "originImageOutput1": [0.1, 0.1, 0.5, 0.2, 0, 0, 0.1, 0, 0, 0],
  "reconsImageOutput1": [0.1, 0.1, 0.5, 0.2, 0, 0, 0.1, 0, 0, 0]
}
```

- 返回值

| code  | chooseError2 |
| :---: | :----------: |
|  20   |  合法无报错  |
|  21   |  图片不合法  |

| code  |    imageNumber1    |
| :---: | :----------------: |
|   1   | 只有原始图像有输出 |
|   2   | 原始和重建图像都有 |

|              code               | originImageOutput1 |
| :-----------------------------: | :----------------: |
| 原始图像的输出,10 个小数,和为 1 |

|              code               | reconsImageOutput1 |
| :-----------------------------: | :----------------: |
| 重建图像的输出,10 个小数,和为 1 |

# Browser 选择鲁棒模型

```json
{
  "command": "robustModel"
}
```

# Server 选择鲁棒模型

```json
{
  "command": "robustModel",
  "chooseError3": 30,
  "imageNumber2": 1,
  "originImageOutput2": [0.1, 0.1, 0.5, 0.2, 0, 0, 0.1, 0, 0, 0],
  "reconsImageOutput2": [0.1, 0.1, 0.5, 0.2, 0, 0, 0.1, 0, 0, 0]
}
```

- 返回值

| code  | chooseError3 |
| :---: | :----------: |
|  30   |  合法无报错  |
|  31   |  图片不合法  |

| code  |    imageNumber2    |
| :---: | :----------------: |
|   1   | 只有原始图像有输出 |
|   2   | 原始和重建图像都有 |

|              code               | originImageOutput2 |
| :-----------------------------: | :----------------: |
| 原始图像的输出,10 个小数,和为 1 |

|              code               | reconsImageOutput2 |
| :-----------------------------: | :----------------: |
| 重建图像的输出,10 个小数,和为 1 |

# Browser 重建防御

```json
{
  "command": "reconsDefense"
}
```

# Server 重建防御

```json
{
  "command": "reconsDefense",
  "chooseError4": 40,
  "imageRecons": "imageRecons"
}
```

- 返回值

| code  | chooseError4 |
| :---: | :----------: |
|  40   |  合法无报错  |
|  41   |  图片不合法  |

|     code     | imageRecons |
| :----------: | :---------: |
| 返回重建图像 |

# Browser 对抗检测

```json
{
  "command": "adverDetection"
}
```

# Server 对抗检测

```json
{
  "command": "adverDetection",
  "chooseError5": 50,
  "imageNumber3": 1,
  "originAdver": 1,
  "originRisk": 0.8,
  "reconsAdver": 1,
  "reconsRisk": 0.8,
  "riskThreshold": 0.7
}
```

- 返回值

| code  | chooseError5 |
| :---: | :----------: |
|  50   |  合法无报错  |
|  51   |  图片不合法  |

| code  |    imageNumber3    |
| :---: | :----------------: |
|   1   | 只有原始图像有输出 |
|   2   | 原始和重建图像都有 |

|        code        | originAdver |
| :----------------: | :---------: |
|         0          |  正常样本   |
|         1          |  对抗样本   |
| 原始图像的检测输出 |

|           code            | originRisk |
| :-----------------------: | :--------: |
| 原始图像风险系数,0~1 之间 |

|        code        | reconsAdver |
| :----------------: | :---------: |
|         0          |  正常样本   |
|         1          |  对抗样本   |
| 重建图像的检测输出 |

|           code            | reconsRisk |
| :-----------------------: | :--------: |
| 重建图像风险系数,0~1 之间 |

|         code          | riskThreshold |
| :-------------------: | :-----------: |
| 风险系数阈值,0~1 之间 |

# Browser 全防御流程

```json
{
  "command": "wholePipeline"
}
```

# Server 全防御流程

```json
{
  "command": "wholePipeline",
  "chooseError6": 60,
  "imageRecons": "imageRecons",
  "chooseError5": 50,
  "imageNumber3": 1,
  "originAdver": 1,
  "originRisk": 0.8,
  "reconsAdver": 1,
  "reconsRisk": 0.8,
  "riskThreshold": 0.7,
  "originImageOutput1": [0.1, 0.1, 0.5, 0.2, 0, 0, 0.1, 0, 0, 0],
  "reconsImageOutput1": [0.1, 0.1, 0.5, 0.2, 0, 0, 0.1, 0, 0, 0],
  "originImageOutput2": [0.1, 0.1, 0.5, 0.2, 0, 0, 0.1, 0, 0, 0],
  "reconsImageOutput2": [0.1, 0.1, 0.5, 0.2, 0, 0, 0.1, 0, 0, 0]
}
```

- 返回值

| code  | chooseError6 |
| :---: | :----------: |
|  60   |  合法无报错  |
|  61   |  图片不合法  |

|     code     | imageRecons |
| :----------: | :---------: |
| 返回重建图像 |

| code  | chooseError5 |
| :---: | :----------: |
|  50   |  合法无报错  |
|  51   |  图片不合法  |

| code  |    imageNumber3    |
| :---: | :----------------: |
|   1   | 只有原始图像有输出 |
|   2   | 原始和重建图像都有 |

|        code        | originAdver |
| :----------------: | :---------: |
|         0          |  正常样本   |
|         1          |  对抗样本   |
| 原始图像的检测输出 |

|           code            | originRisk |
| :-----------------------: | :--------: |
| 原始图像风险系数,0~1 之间 |

|        code        | reconsAdver |
| :----------------: | :---------: |
|         0          |  正常样本   |
|         1          |  对抗样本   |
| 重建图像的检测输出 |

|           code            | reconsRisk |
| :-----------------------: | :--------: |
| 重建图像风险系数,0~1 之间 |

|         code          | riskThreshold |
| :-------------------: | :-----------: |
| 风险系数阈值,0~1 之间 |

|              code               | originImageOutput1 |
| :-----------------------------: | :----------------: |
| 原始图像的输出,10 个小数,和为 1 |

|              code               | reconsImageOutput1 |
| :-----------------------------: | :----------------: |
| 重建图像的输出,10 个小数,和为 1 |

|              code               | originImageOutput2 |
| :-----------------------------: | :----------------: |
| 原始图像的输出,10 个小数,和为 1 |

|              code               | reconsImageOutput2 |
| :-----------------------------: | :----------------: |
| 重建图像的输出,10 个小数,和为 1 |

# Browser 物理世界平台

```json
{
  "command": "realWorldPlatform",
  "camera": "frame"
}
```

|         code         | frame |
| :------------------: | :---: |
| 摄像头实时采集的图像 |

# Server 物理世界平台

```json
{
  "command": "realWorldPlatform",
  "chooseError7": 70,
  "imageProcess": "imageProcess",
  "realtimeOutput": [0.1, 0.1, 0.5, 0.2, 0, 0, 0.1, 0, 0, 0]
}
```

- 返回值

| code  | chooseError7 |
| :---: | :----------: |
|  70   |  合法无报错  |
|  71   |  图片不合法  |

|      code      | imageProcess |
| :------------: | :----------: |
| 返回处理后图像 |

|             code              | realtimeOutput |
| :---------------------------: | :------------: |
| 实时概率输出,10 个小数,和为 1 |
