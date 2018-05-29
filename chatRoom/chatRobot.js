export class Person {
    constructor(config) {
        this.config = config || {};
        this.replyList = [];
        this.init();
    }

    init() {
        this.frame = this.config.frame;

        this.document = this.frame.contentDocument;

        this.replyTarget = null;
        this.replyInterval = 1000;

        // 添加接受消息的input
        var messageInput = document.createElement('input');
        messageInput.setAttribute('type', 'text');
        messageInput.value = '';
        this.$receivedMessageContainer = messageInput;

        // 添加事件监听message变化
        let vm = this;
        this.updateReceivedMessageEvent = new Event('update');

        // 添加监听window message变化
        this.showReplyByPostMessage();

        messageInput.addEventListener('update', (e) => {
            vm.receivedMessage = e.target.value;

            

            vm.think()
                .then(sleep(this.replyInterval))
                .then(successHandler)
                .then(filterResult)
                .then(vm.reply.bind(vm))
                .then(vm.sayByPostMessage.bind(vm))
                .catch(errorHandler);
        });

        this.document.body.appendChild(messageInput);
    }
    reply(responseText) {

        this.replyList.push(responseText);
        if (this.replyTarget instanceof Person) {
            this.sayTo(this.replyTarget, responseText);
        }
        
        return responseText;
    }

    think() {
        return postMessage(this.receivedMessage, this.config.user)
    }

    sayByPostMessage(responseText) {
        this.frame.contentWindow.postMessage(responseText, location.origin);
    }

    showReplyByPostMessage() {
        this.frame.contentWindow.onmessage = (evt) => console.log(evt);   
    }

    receiveMessage(text) {
        this.$receivedMessageContainer.value = text;
        this.$receivedMessageContainer.dispatchEvent(this.updateReceivedMessageEvent);
    }

    sayTo (person, message) {
        let vm = this;
        if (person instanceof Person) {
            person.receiveMessage(message);
            person.replyTarget = vm;
        }
    }

    replySpeed (timeInterval) {
        if (typeof timeInterval === 'number' && timeInterval > 1000) {
            this.replyInterval = timeInterval || 1000;
        } else {
            this.replyInterval = 1000;
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

