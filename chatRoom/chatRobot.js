export class Person {
    constructor(config) {
        let vm = this;

        this.config = config || {};

        // 回复的对象
        this.replyTarget = null;

        // 回复的时间间隔
        this.replyInterval = 1000;

        this.customEvent = this.initCustomEvent('update');

        this.hasReplied = false;

        // 默认回复方法
        this.method = 'broadcastChannel';

        // 创建一个自己的专属channel
        this.selfBroadcastChannel = new BroadcastChannel(this.config.user.name);

        // 初始化对话控制状态
        this.replyStatus = true;

        // 初始化相关事件
        this.initEvents();

        // 初始化相关DOM
        this.initDoms();
        // 关闭页面时销毁相关事件
        window.onunload = () => {
            vm.destory();
        }
    }

    initDoms() {
        // 初始化是否回复按钮
        if (this.config.replyButton && this.config.replyButton.nodeType === 1) {
            let replyButtonHandler = function (e) {
                this.changeReplyStatus(e.target.checked);
            }

            this.config.replyButton.addEventListener('change', replyButtonHandler.bind(vm))
        }
    }

    initEvents() {
        // 接受消息的属性
        this.$receivedMessage = document.createElement('input');
        this.$receivedMessage.type = 'text';
        this.$receivedMessage.value = '';
        this.$receivedMessage.addEventListener('update', this.receivedMessageUpdateHandler.bind(this));

        // 装载回复消息的容器
        this.$replyMessage = document.createElement('input');
        this.$replyMessage.type = 'text';
        this.$replyMessage.value = '';
        this.$replyMessage.addEventListener('update', this.replyMessageUpdateHandler.bind(this));

    }

    initCustomEvent(customEventName) {
        return new Event(customEventName);
    }

    receivedMessageUpdateHandler(e) {
        let vm = this;
        if (vm.replyStatus) {
            vm.think()
                .then(sleep(vm.replyInterval))
                .then(successHandler)
                .then(filterResult)
                .then(vm.confirmReplyMessage.bind(vm))
                .catch(errorHandler);
        } else {
            console.log('思考回复消息失败')
        }
    }

    // 回复语句更新后的处理方法
    replyMessageUpdateHandler(e) {
        console.log('send message: ' + this.$replyMessage.value);
        if (this.method === 'localStorage') {
            window.localStorage[this.localStorageKey[0]] = this.$replyMessage.value;
        } else if (this.method === 'broadcastChannel') {
            // 通过BroadcastChannel传递消息
            this.sendMessageByBroadcastChannel();
        }
    }

    confirmReplyMessage(message) {
        this.replyMessageUpdate(message);
    }

    handleReceivedMessage() {
        let vm = this;

        if (vm.replyStatus) {
            // 回复完成，重置是否回复过的状态
            vm.hasReplied = false;

            return vm.think()
                .then(sleep(vm.replyInterval))
                .then(successHandler)
                .then(filterResult)
        } else {
            console.log('Have already stop reply');
        }

    }

    think() {
        return postMessage(this.$receivedMessage.value, this.config.user)
    }

    // 使用BroadcastChannel发送消息
    sendMessageByBroadcastChannel() {
        let message = this.$replyMessage.value;
        if (typeof message === 'string') {
            this.selfBroadcastChannel.postMessage(message);
        } else {
            throw new Error('message not exist');
        }
    }

    // 使用BroadcastChannel接收消息
    receiveMessageByBroadcastChannel(targetPersonName) {

        let vm = this;

        if (typeof targetPersonName === 'string' && targetPersonName.length) {
            let listeningChannel = new BroadcastChannel(targetPersonName);
            listeningChannel.onmessage = (e) => {
                vm.receivedMessageUpdate(e.data);

            }
        }
    }


    // 建立localStorage通信机制
    communicateByLocalStorage(targetPersonName) {
        let vm = this;

        if (typeof targetPersonName === 'string' && targetPersonName.length) {
            window.localStorage.setItem(`${this.config.user.name}To${targetPersonName}`, '');
            window.localStorage.setItem(`${targetPersonName}To${this.config.user.name}`, '');

            vm.localStorageKey = [`${this.config.user.name}To${targetPersonName}`
                , `${targetPersonName}To${this.config.user.name}`];

            vm.receiveMessageByLocalStorage();

        }
    }


    // 将消息通过localStorage送出去
    sendMessageByLocalStorage() {
        window.localStorage.setItem(`${this.config.user.name}To${this.targetPersonName}`, this.$receivedMessage.value);
    }

    // 接受通过localStorage传回来的消息
    receiveMessageByLocalStorage() {
        let receiveMessageHandler = function (e) {
            // 监听接收消息的storageItem是否有变动
            if (e.key === this.localStorageKey[1]) {
                this.receivedMessageUpdate(window.localStorage[this.localStorageKey[1]]);

            }
        }

        window.onstorage = receiveMessageHandler.bind(this);
    }

    receivedMessageUpdate(value) {
        this.$receivedMessage.value = value;
        console.log('received message: ' + value);
        this.$receivedMessage.dispatchEvent(this.customEvent);
    }

    replyMessageUpdate(value) {
        this.$replyMessage.value = value;
        this.$replyMessage.dispatchEvent(this.customEvent);
    }

    // 控制是否回复
    changeReplyStatus(status) {
        if (typeof status === 'boolean') {
            this.replyStatus = status;
            console.log('调整回复状态为：' + this.replyStatus);
            if (this.replyStatus) {
                this.handleReceivedMessage();
            }
        }
    }

    // 控制回复速度
    replySpeed(timeInterval) {
        if (typeof timeInterval === 'number' && timeInterval > 1000) {
            this.replyInterval = timeInterval || 1000;
        } else {
            this.replyInterval = 1000;
        }
    }

    // 开始一个话题
    beginTalk(targetPersonName, method = 'broadcastChannel', startMessage) {
        this.targetPersonName = targetPersonName;
        this.method = method;

        if (typeof startMessage === 'string' && startMessage.length) {
            if (method == 'localStorage') {

                this.communicateByLocalStorage(targetPersonName);
                this.replyMessageUpdate(startMessage);
            } else {
                this.receiveMessageByBroadcastChannel(targetPersonName);
                this.replyMessageUpdate(startMessage);
            }
        } else {
            if (method == 'localStorage') {

                this.communicateByLocalStorage(targetPersonName);
            } else {
                this.receiveMessageByBroadcastChannel(targetPersonName);
            }
        }
    }

    destory() {
        this.$receivedMessage.removeEventListener('update', this.receivedMessageUpdateHandler.bind(this));
        this.$replyMessage.removeEventListener('update', this.replyMessageUpdateHandler.bind(this));

        // 关闭broadcastChannel通道
        this.selfBroadcastChannel.close();
    }
}

function postMessage(message, user) {
    if (!message || typeof message != 'string') {
        return;
    }

    const url = 'http://openapi.tuling123.com/openapi/api/v2';

    const defaultData = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": message
            },
            "selfInfo": {
                "location": {
                    "city": "北京",
                    "province": "北京",
                    "street": "信息路"
                }
            }
        },
        "userInfo": {
            "apiKey": user.apiKey,
            "userId": user.userId
        }
    }

    return axios.post(url, defaultData);
}

function sleep(ms) {
    return function (value) {
        return new Promise((resolve) => {
            setTimeout(() => resolve(value), ms);
        })

    }
}

function errorHandler(error) {
    console.log(error)
}

function successHandler(res) {
    if (res.status === 200) {
        return res.data;
    } else {
        throw new Error(res.statusText);
    }
}

function filterResult(res) {
    let result = res.results;
    let text = '';

    for (let item of result) {
        text += item.values.text;
    }

    return text;
}

