let params = {
    url: 'http://freegeoip.net/json/',
    callbackName: 'responseHandle',
    jsonp: true,
    time: 1000,
    success: () => {},
    error: (message) => {
        alert(message);
    }
};

function jsonp (params) {
    if (typeof params !== 'object' || !(params.jsonp)) {
        return;
    }

    // 创建script标签并插入到页面
    let $script = document.createElement('script');
    let $head = document.getElementsByTagName('head')[0];
    $head.appendChild($script);

    // 设置传递给后台的回调函数名 
    let callbackName = params.callbackName;
    let url = `${params.url}?callback=${callbackName}`;

    // 创建回调函数
    window[callbackName] = (data) => {
        // 接收到本次回调后，移除相关全局属性，script标签，清除计时器
        $head.removeChild($script);
        clearTimeout($script.timer);
        window[callbackName] = null;

        // 成功后的数据处理
        params.success && params.success(data);
    }

    // 发送请求
    $script.src = url;

    // 为了判断请求是否成功，设置超时处理
    if (params.time) {
        $script.timer = setTimeout(() => {
            // 接收到本次回调后，移除相关全局属性，script标签，清除计时器
            $head.removeChild($script);
            window[callbackName] = null;

            // 超时后的错误处理
            params.error && params.error('请求超时');
        }, params.time)
    }
    
}