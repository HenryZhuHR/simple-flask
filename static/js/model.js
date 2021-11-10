
function setProgress(id, json_predict) {
    console.log(json_predict)
    for (var class_name in json_predict) {
        document.querySelector("#" + id + " #" + class_name + " .progress-done").setAttribute("data-done", parseInt(json_predict[class_name] * 100).toString());
        document.querySelector("#" + id + " #" + class_name + " .percent").innerHTML = (json_predict[class_name] * 100).toFixed(1).toString();
    }
    update_progress();
}


function robust_model() {
    var httpRequest = new XMLHttpRequest();     //第一步：创建需要的对象
    httpRequest.open('POST', '/api/robust_model', true);    //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
    httpRequest.setRequestHeader("Content-type", "application/json");   //设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）var obj = { name: 'zhansgan', age: 18 };
    httpRequest.send(JSON.stringify({}));   //发送请求 将json写入send中

    httpRequest.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
        if (httpRequest.readyState == 4 && httpRequest.status == 200) { //验证请求是否发送成功
            var result = httpRequest.responseText;    //获取到服务端返回的数据
            json_result = JSON.parse(result);  // 使用静态方法JSON.parse()，将字符串解析为对象。

            if (json_result.hasOwnProperty("Error")) {
                console.log("Error");
            }
            else {
                document.getElementById("original_image").setAttribute("src", "data:image/png;base64," + json_result["image"]);
                setProgress("originalImage-robustModel", json_result["predict"]);

            }
        }
        else {   // 请求发送失败。报错
            console.log("httpRequest Error");
        }
    };
}

function reconstructed_model() {
    var httpRequest = new XMLHttpRequest();     //第一步：创建需要的对象
    httpRequest.open('POST', '/api/reconstructed_model', true);    //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
    httpRequest.setRequestHeader("Content-type", "application/json");   //设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）var obj = { name: 'zhansgan', age: 18 };
    httpRequest.send(JSON.stringify({}));   //发送请求 将json写入send中

    httpRequest.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
        if (httpRequest.readyState == 4 && httpRequest.status == 200) { //验证请求是否发送成功
            var result = httpRequest.responseText;    //获取到服务端返回的数据
            json_result = JSON.parse(result);  // 使用静态方法JSON.parse()，将字符串解析为对象。

            if (json_result.hasOwnProperty("Error")) {
                console.log("Error");
                console.log(json_result["Error"])
            }
            else {
                console.log("data:image/png;base64," + json_result["image"])
                document.getElementById("reconstructed_image").setAttribute("src", "data:image/png;base64," + json_result["image"]);
            }
        }
        else {   // 请求发送失败。报错
            console.log("httpRequest Error");
            console.log(httpRequest.readyState);
            console.log(httpRequest.status);
        }
    };
}