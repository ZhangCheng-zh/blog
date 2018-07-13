// Object.defineProperty
let obj1 = {};
let a;

Object.defineProperty(obj1, 'a', {
    get: function () {
        console.log('get val');
    },
    set: function (val) {
        console.log('set val');
        return val;
    }
})

// 订阅者模式

// 主题对象，收集发布者消息，通知订阅者更新
class Dep {
    constructor () {
        // 订阅者队列
        this.subs = [];
    }
    addSub (sub) {
        this.subs.push(sub);
    }
    // 通知所有订阅者更新
    notify () {
        this.subs.forEach((item) => {
            // 订阅者依次更新
            item.update();
        })
    }
}

// 订阅者
class Sub {
    constructor (x) {
        this.x = x;
    }
    // 订阅者的具体更新动作
    update () {
        this.x = this.x + 1;
        console.log(this.x);
    }
}

//  发布者
class Pub {
    constructor () {
        this.dep = new Dep();
    }
    addSub (sub) {
        this.dep.addSub(sub);
    }
    // 发布动作
    publish () {
        // 让订阅者依次更新
        this.dep.notify(); 
    }
}


let pub1 = new Pub();

pub1.addSub(new Sub(1));




