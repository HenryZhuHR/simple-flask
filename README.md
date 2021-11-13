# API 文档

[API 文档](http://henryzhuhr.xyz/simple-flask/)

<!-- 
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
| 实时概率输出,10 个小数,和为 1 | -->
