export class Person {
    constructor(config) {
        this.config = config || {};
        this.replyList = [];
        // 回复的对象
        this.replyTarget = null;

        // 回复的时间间隔
        this.replyInterval = 1000;

        // 接受消息的属性
        this.$receivedMessage = document.createElement('input');
        this.$receivedMessage.type = 'text';
        this.$receivedMessage.value = '';

        // 初始化对话控制状态
        this.status = {
            silent: false,
            stop: false,
        }

        // 创建一个自己的专属channel
        this.selfBroadcastChannel = new BroadcastChannel(this.config.user.name);

        // 给接受message的变量绑定监听更新的事件
        this.receivedMessageContainerAddEvent();


        let vm = this;

        // 关闭页面时销毁相关事件
        window.onunload = () => {
            vm.destory();
        }
    }

    destory () {
        this.selfBroadcastChannel.close();
    }

    receivedMessageContainerAddEvent () {
        let vm = this;
        
        vm.receivedMessageUpdateEvent = new Event('updateMessage', { "bubbles": false, "cancelable": true });

        let updateHandler = function (e) {
            debugger;
            return vm.think()
                .then(sleep(vm.replyInterval))
                .then(successHandler)
                .then(filterResult)
                .then(vm.reply)
                .then(vm.sendMessageByBroadcastChannel)
                .catch(errorHandler);
        }

        vm.$receivedMessage.addEventListener('updateMessage', updateHandler.bind(vm));
    }

    reply(responseText) {
        this.replyList.push(responseText);

        if (this.replyTarget instanceof Person) {
            this.sayTo(this.replyTarget, responseText);
            debugger;
        }

        return responseText;
    }

    think() {
        return postMessage(this.$receivedMessage.value, this.config.user)
    }

    sayByPostMessage(responseText) {
        this.replyTarget.postMessage(responseText, location.origin);
    }

    showReplyByPostMessage() {
        this.replyTarget.onmessage = (evt) => console.log(evt);
    }

    sendMessageByBroadcastChannel(message) {
        if (typeof message === 'string') {
            console.log('send message: ' + message);
            this.selfBroadcastChannel.postMessage(message);
        } else {
            throw new Error('message not exist');
        }
    }

    communicateByBroadcastChannel(targetPersonName) {
        let vm = this;
        if (targetPersonName) {
            let listeningChannel = new BroadcastChannel(targetPersonName);
            listeningChannel.onmessage = (e) => vm.receiveMessage(e.data)
        }
    }

    receiveMessage(text) {
        let vm = this;

        vm.$receivedMessage.value = text;
        console.log('received message: ' + text);

        vm.$receivedMessage.dispatchEvent(vm.receivedMessageUpdateEvent);
    }

    toggleTalk() {
        this.status.stop = !(this.status.stop);

        if (this.status.stop) {

        }
    }

    sayTo(person, message) {
        let vm = this;
        if (person instanceof Person) {
            person.receiveMessage(message);
            person.replyTarget = vm;
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
    beginTalk(startMessage) {
        if (typeof startMessage === 'string' && startMessage.length) {
            this.sendMessageByBroadcastChannel(startMessage);
        } else {
            throw new Error('Start message not match rules.');
        }
    }

    // 终止一次对话
    finishTalk() {

    }

    // 暂停当前对话
    stopTalk() { }

    // 恢复当前对话
    resumeTalk() { }
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

