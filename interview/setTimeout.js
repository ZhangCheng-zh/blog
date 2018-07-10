// 基础版
// 考点： 
// 1 i是全局变量
// 2 异步执行的执行顺序
for (var i = 0; i < 5; i++) {
    setTimeout(() => {
        console.log(new Date(), i);
    }, 1000);
}

console.log(new Date(), i);


// 进阶1：如何让打印数字阶梯上涨
for (var i = 0; i < 5; i++) {
    ((i) => {
        setTimeout(() => {
            console.log(new Date(), i);
        }, 1000);
    })(i)
}

console.log(new Date(), i);

// 进阶： 如何使用让setTimeout中的打印优先执行
new Promise(function (resolve, reject) {
    for (var i = 0; i < 5; i++) {
        if (i === 4) {
            setTimeout(() => {
                console.log(new Date(), i);
                resolve(10);
            }, 1000);
        } else {
            setTimeout(() => {
                console.log(new Date(), i);
            }, 1000);
        }

    }
}).
then((val) => console.log(new Date(), val));