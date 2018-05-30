export class Person {
    constructor(config) {
        let vm = this;

        this.config = config || {};
        this.replyList = [];


        this.latestReply = ''
        // 回复的对象
        this.replyTarget = null;

        // 回复的时间间隔
        this.replyInterval = 1000;

        this.customEvent = this.initCustomEvent('update');

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

        this.hasReplied = false;

        // 默认回复方法
        this.method = 'broadcastChannel';



        // 创建一个自己的专属channel
        this.selfBroadcastChannel = new BroadcastChannel(this.config.user.name);

        // 初始化对话控制状态
        this.replyStatus = true;

        // 初始化是否回复按钮
        if (this.config.replyButton && this.config.replyButton.nodeType === 1) {
            this.config.replyButton.addEventListener('change', (e) => {
                // debugger;
                vm.changeReplyStatus(e.target.checked);
            })
        }

        // 关闭页面时销毁相关事件
        window.onunload = () => {
            vm.destory();
        }
    }

    initCustomEvent(customEventName) {
        return new Event(customEventName);
    }

    receivedMessageUpdateHandler(e) {
        let vm = this;
        if (this.replyStatus) {
            this.think()
                .then(sleep(vm.replyInterval))
                .then(successHandler)
                .then(filterResult)
                .then(vm.confirmReplyMessage.bind(vm))
                .catch(errorHandler)
        } else {
            console.log('思考回复消息失败')
        }
    }

    // 回复语句更新后的处理方法
    replyMessageUpdateHandler(e) {
        if (this.method === 'localStorage') {
            this.sendMessageByLocalStorage();
        } else if (this.method === 'broadcastChannel') {
            // 通过BroadcastChannel传递消息
            this.sendMessageByBroadcastChannel();
        }
    }

    confirmReplyMessage(message) {
        this.replyMessageUpdate(message);
    }

    destory() {
        this.selfBroadcastChannel.close();
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
            console.log('send message: ' + message);
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
                vm.receivedMessageUpdate.bind(vm);
            }
        }
    }


    // 建立localStorage通信机制
    communicateByLocalStorage(targetPersonName) {
        let vm = this;

        if (typeof targetPersonName === 'string' && targetPersonName.length) {
            vm.initLocalStorageCommunication(targetPersonName);
        }
    }

    // 初始化localStorage的通信通道
    initLocalStorageCommunication(targetPersonName) {
        let vm = this;

        window.localStorage.setItem(`${this.config.user.name}To${targetPersonName}`, '');
        window.localStorage.setItem(`${targetPersonName}To${this.config.user.name}`, '');

        vm.localStorageKey = [`${this.config.user.name}To${targetPersonName}`
            , `${targetPersonName}To${this.config.user.name}`];


    }

    // 将消息通过localStorage送出去
    sendMessageByLocalStorage(message) {
        window.localStorage.setItem(`${this.config.user.name}To${targetPersonName}`, message);
    }

    // 接受通过localStorage传回来的消息
    receiveMessageByLocalStorage(message) {
        window.onstorage = e => {
            // 监听接收消息的storageItem是否有变动
            if (e.key === vm.localStorageKey[1]) {
                vm.receivedMessageUpdate();
            }
        }
    }

    receivedMessageUpdate(value) {
        this.$receivedMessage.value = value;
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

    replySpeed(timeInterval) {
        if (typeof timeInterval === 'number' && timeInterval > 1000) {
            this.replyInterval = timeInterval || 1000;
        } else {
            this.replyInterval = 1000;
        }
    }

    // 开始一个话题
    beginTalk(startMessage, method) {
        if (typeof startMessage === 'string' && startMessage.length) {
            if (method == 'localStorage') {

            }
        } else {
            throw new Error('Start message not match rules.');
        }
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

