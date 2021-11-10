# 上传图片
调用此 API ，可以上传图片到服务器上，并且暂存到后台，以供其他程序，例如 [鲁棒模型](api/robust_model.md) 直接调用

## 1.接口描述

接口地址：`/api/upload_image`

请求方法：POST

## 2.输入参数

| 请求参数 | 必选 | 类型   | 描述                                     |
| :------- | :--- | :----- | :--------------------------------------- |
| image    | 是   | base64 | 上传服务器的图片需要以 base64 的格式传递 |

## 3.输出参数

| 返回参数  | 描述                                |
| :-------- | :---------------------------------- |
| status | 上传状态，一般为 `Success`          |
| Error     | 包含错误码`Code`和错误提示`Message` |

## 4.示例

**输入示例**
```curl
POST /api/upload_image HTTP/1.1
Content-Type: application/json

{
    "image":<base_64_image>,
}
```

**输出示例**
```json
{
    "status": "Success"
}
```

**错误返回实例**
```json
"Error": {
    "Code": "SelectImage.FileNotFound",
    "Message": "request image file adv_101802.png not found"
}
```

## 5.错误码
| 错误码                       | 描述                             |
| :--------------------------- | :------------------------------- |
| NotParameterGet              | 参数值错误或未获取参数值。       |
| UploadImage.LossParameter    | 缺少参数。                       |
| UploadImage.DecodeImageError | 图片进行 base64 编码时发生错误。 |
