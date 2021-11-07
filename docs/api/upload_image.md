# 上传图片
调用此 API ，可以上传图片到服务器上，并且暂存到后台，以供其他程序，例如 [鲁棒模型]() 直接调用

## 1.接口描述

接口地址：`/upload_image`

请求方法：POST

## 2.输入参数

| 请求参数  | 必选 | 类型   | 描述                       |
| :-------- | :--- | :----- | :------------------------- |
| file_name | 是   | String | 需要选择服务器上的图片文件 |

## 3.输出参数

| 返回参数 | 描述                                |
| :------- | :---------------------------------- |
| image    | 经过base64编码的图片数据            |
| Error    | 包含错误码`Code`和错误提示`Message` |

## 4.示例

**输入示例**
```curl
POST /upload_image HTTP/1.1
Content-Type: application/json

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

**错误返回实例**
```json
'Error': {
    'Code': 'SelectImage.FileNotFound',
    'Message': 'request image file adv_101802.png not found'
}
```

## 5.错误码
| 错误码                            | 描述             |
| :-------------------------------- | :--------------- |
| SelectImage.InvalidParameterValue | 参数值错误。     |
| SelectImage.FileNotFound          | 没有此图片文件。 |
