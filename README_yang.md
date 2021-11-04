


测试基于 Flask 框架

# Browser选择图像
```json
{
    "command": "chooseImage",
    "imageOrigin":"/**/image.jpg"
}
```
# Server选择图像
```json
{
    "command": "chooseImage",
    "chooseError": 00,
    "imageOrigin":"imageOrigin"
}
```
- 返回值

| code  | chooseError |
| :---: | :--------:  |
|  00   | 合法无报错   |
|  01   | 图片不合法   |

| code  | imageOrigin |
| :---: | :--------:  |
|      返回原始图像    |


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
    "chooseError1": 10,
    "imageNumber1": 1,
    "originImageOutput1": [0.1, 0.1, 0.5, 0.2, 0, 0, 0.1, 0, 0, 0],
    "reconsImageOutput1": [0.1, 0.1, 0.5, 0.2, 0, 0, 0.1, 0, 0, 0]
}
```
- 返回值

| code  | chooseError1 |
| :---: | :--------:   |
|  10   | 合法无报错    |
|  11   | 图片不合法    |

| code  | imageNumber1       |
| :---: | :----------------: |
|   1   | 只有原始图像有输出   |
|   2   | 原始和重建图像都有   |

| code  | originImageOutput1  |
| :---: | :----------------:  |
| 原始图像的输出,10个小数,和为1 |

| code  | reconsImageOutput1  |
| :---: | :----------------:  |
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
    "chooseError2": 20,
    "imageNumber2": 1,
    "originImageOutput2": [0.1, 0.1, 0.5, 0.2, 0, 0, 0.1, 0, 0, 0],
    "reconsImageOutput2": [0.1, 0.1, 0.5, 0.2, 0, 0, 0.1, 0, 0, 0]
}
```
- 返回值

| code  | chooseError2 |
| :---: | :--------:   |
|  20   | 合法无报错    |
|  21   | 图片不合法    |

| code  | imageNumber2       |
| :---: | :----------------: |
|   1   | 只有原始图像有输出   |
|   2   | 原始和重建图像都有   |

| code  | originImageOutput2  |
| :---: | :----------------:  |
| 原始图像的输出,10个小数,和为1 |

| code  | reconsImageOutput2  |
| :---: | :----------------:  |
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
    "chooseError3": 30,
    "imageRecons": "imageRecons"
}
```
- 返回值

| code  | chooseError3 |
| :---: | :--------:   |
|  30   | 合法无报错    |
|  31   | 图片不合法    |

| code  | imageRecons |
| :---: | :--------:  |
|      返回重建图像    |


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
    "chooseError4": 40,
    "imageNumber3": 1,
    "originAdver": 1,
    "originRisk": 0.8,
    "reconsAdver": 1,
    "reconsRisk": 0.8,
    "riskThreshold": 0.7
}
```

- 返回值

| code  | chooseError4 |
| :---: | :--------:   |
|  40   | 合法无报错    |
|  41   | 图片不合法    |

| code  | imageNumber3       |
| :---: | :----------------: |
|   1   | 只有原始图像有输出   |
|   2   | 原始和重建图像都有   |

| code  | originAdver |
| :---: | :--------:  |
|  0    | 正常样本     |
|  1    | 对抗样本     |
|  原始图像的检测输出   |

| code  | originRisk     |
| :---: | :--------:     |
| 原始图像风险系数,0~1之间 |

| code  | reconsAdver |
| :---: | :--------:  |
|  0    | 正常样本     |
|  1    | 对抗样本     |
|  重建图像的检测输出   |

| code  | reconsRisk     |
| :---: | :--------:     |
| 重建图像风险系数,0~1之间 |

| code  | riskThreshold  |
| :---: | :--------:     |
|   风险系数阈值,0~1之间   |



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
    "chooseError5": 50,
    "imageRecons": "imageRecons",
    "chooseError4": 40,
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
| code  | chooseError5 |
| :---: | :--------:   |
|  50   | 合法无报错    |
|  51   | 图片不合法    |

| code  | imageRecons |
| :---: | :--------:  |
|      返回重建图像    |

| code  | chooseError4 |
| :---: | :--------:   |
|  40   | 合法无报错    |
|  41   | 图片不合法    |

| code  | imageNumber3       |
| :---: | :----------------: |
|   1   | 只有原始图像有输出   |
|   2   | 原始和重建图像都有   |

| code  | originAdver |
| :---: | :--------:  |
|  0    | 正常样本     |
|  1    | 对抗样本     |
|  原始图像的检测输出   |

| code  | originRisk     |
| :---: | :--------:     |
| 原始图像风险系数,0~1之间 |

| code  | reconsAdver |
| :---: | :--------:  |
|  0    | 正常样本     |
|  1    | 对抗样本     |
|  重建图像的检测输出   |

| code  | reconsRisk     |
| :---: | :--------:     |
| 重建图像风险系数,0~1之间 |

| code  | riskThreshold  |
| :---: | :--------:     |
|   风险系数阈值,0~1之间   |

| code  | originImageOutput1  |
| :---: | :----------------:  |
| 原始图像的输出,10个小数,和为1 |

| code  | reconsImageOutput1  |
| :---: | :----------------:  |
| 重建图像的输出,10个小数,和为1 |

| code  | originImageOutput2  |
| :---: | :----------------:  |
| 原始图像的输出,10个小数,和为1 |

| code  | reconsImageOutput2  |
| :---: | :----------------:  |
| 重建图像的输出,10个小数,和为1 |


# Browser物理世界平台
```json
{
    "command": "realWorldPlatform",
    "camera": "frame"
}
```

| code  | frame        |
| :---: | :--------:   |
|  摄像头实时采集的图像  |

# Server物理世界平台
```json
{
    "command": "realWorldPlatform",
    "chooseError6": 60,
    "imageProcess": "imageProcess",
    "realtimeOutput": [0.1, 0.1, 0.5, 0.2, 0, 0, 0.1, 0, 0, 0]
}
```
- 返回值
| code  | chooseError6 |
| :---: | :--------:   |
|  60   | 合法无报错    |
|  61   | 图片不合法    |

| code  | imageProcess |
| :---: | :--------:   |
|     返回处理后图像    |

| code  | realtimeOutput    |
| :---: | :----------------:|
| 实时概率输出,10个小数,和为1 |
