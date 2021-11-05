# 初步拟定接口(草稿)
- [初步拟定接口(草稿)](#初步拟定接口草稿)
- [Client](#client)
  - [选择图片服务器](#选择图片服务器)
- [Browser选择图像](#browser选择图像)
- [Server选择图像](#server选择图像)
- [Browser选择原始模型](#browser选择原始模型)
- [Server选择原始模型](#server选择原始模型)
- [Browser选择鲁棒模型](#browser选择鲁棒模型)
- [Server选择鲁棒模型](#server选择鲁棒模型)
- [Browser重建防御](#browser重建防御)
- [Server重建防御](#server重建防御)
- [Browser对抗检测](#browser对抗检测)
- [Server对抗检测](#server对抗检测)
- [Browser全防御流程](#browser全防御流程)
- [Server全防御流程](#server全防御流程)
- [Browser物理世界平台](#browser物理世界平台)
- [Server物理世界平台](#server物理世界平台)


# Client
POST 请求

| 参数名称 | 必选 | 类型   | 描述 |
| :------- | :--- | :----- | :--- |
| command  | 是   | String | 是   |  |

- 错误码

## 选择图片服务器
请求 url=`/select_image/`

POST 请求
| 参数名称  | 必选 | 类型   | 描述 |
| :-------- | :--- | :----- | :--- |
| file_name | 是   | String | 是   | 调用服务器的参数 |

输入示例:
```bash
{
    "file_name":"./image.jpg"
}
```
输出示例
```bash
{
    "file_name":"./image.jpg"
}
```

# Browser选择图像
POST 请求
```json
{
    "command": "chooseImage",
    "image_name":"/**/image.jpg"
}
```
|    key     |   value    |
| :--------: | :--------: |
|  command   | 合法无报错 |
| image_name | 图片不合法 |
# Server选择图像
```json
{
    "command": "chooseImage",
    "statement": 10,
    "imageOrigin":"imageOrigin"
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


# Browser选择原始模型
```json
{
    "command": "originModel"
}
```
# Server选择原始模型
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

|             code              | originImageOutput1 |
| :---------------------------: | :----------------: |
| 原始图像的输出,10个小数,和为1 |

|             code              | reconsImageOutput1 |
| :---------------------------: | :----------------: |
| 重建图像的输出,10个小数,和为1 |


# Browser选择鲁棒模型
```json
{
    "command": "robustModel"
}
```
# Server选择鲁棒模型
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

|             code              | originImageOutput2 |
| :---------------------------: | :----------------: |
| 原始图像的输出,10个小数,和为1 |

|             code              | reconsImageOutput2 |
| :---------------------------: | :----------------: |
| 重建图像的输出,10个小数,和为1 |


# Browser重建防御
```json
{
    "command": "reconsDefense"
}
```
# Server重建防御
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


# Browser对抗检测
```json
{
    "command": "adverDetection"
}
```
# Server对抗检测
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

|           code           | originRisk |
| :----------------------: | :--------: |
| 原始图像风险系数,0~1之间 |

|        code        | reconsAdver |
| :----------------: | :---------: |
|         0          |  正常样本   |
|         1          |  对抗样本   |
| 重建图像的检测输出 |

|           code           | reconsRisk |
| :----------------------: | :--------: |
| 重建图像风险系数,0~1之间 |

|         code         | riskThreshold |
| :------------------: | :-----------: |
| 风险系数阈值,0~1之间 |



# Browser全防御流程
```json
{
    "command": "wholePipeline"
}
```
# Server全防御流程
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

|           code           | originRisk |
| :----------------------: | :--------: |
| 原始图像风险系数,0~1之间 |

|        code        | reconsAdver |
| :----------------: | :---------: |
|         0          |  正常样本   |
|         1          |  对抗样本   |
| 重建图像的检测输出 |

|           code           | reconsRisk |
| :----------------------: | :--------: |
| 重建图像风险系数,0~1之间 |

|         code         | riskThreshold |
| :------------------: | :-----------: |
| 风险系数阈值,0~1之间 |

|             code              | originImageOutput1 |
| :---------------------------: | :----------------: |
| 原始图像的输出,10个小数,和为1 |

|             code              | reconsImageOutput1 |
| :---------------------------: | :----------------: |
| 重建图像的输出,10个小数,和为1 |

|             code              | originImageOutput2 |
| :---------------------------: | :----------------: |
| 原始图像的输出,10个小数,和为1 |

|             code              | reconsImageOutput2 |
| :---------------------------: | :----------------: |
| 重建图像的输出,10个小数,和为1 |


# Browser物理世界平台
```json
{
    "command": "realWorldPlatform",
    "camera": "frame"
}
```

|         code         | frame |
| :------------------: | :---: |
| 摄像头实时采集的图像 |

# Server物理世界平台
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

|            code             | realtimeOutput |
| :-------------------------: | :------------: |
| 实时概率输出,10个小数,和为1 |
