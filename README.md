


测试基于 Flask 框架

# json 格式
```json
{
    "command": "robustModel",
    "image":"image"
}
```

- 命令列表
|   command   |    code    |
| :---------: | :--------: |
| robustModel | 0002之类的 |

- 返回值

| code  |   error    |
| :---: | :--------: |
|  10   | 合法无报错 |
|  11   | 图片不合法 |

| code  |     error      |
| :---: | :------------: |
|  20   | 接收到非法数据 |
|  21   |   图片不合法   |