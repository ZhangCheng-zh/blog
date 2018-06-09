function debounce (fn, limit) {
    const _this = this;

    let timeoutId = null;

    return function (...args) {
        // 如果上一个动作还没有完成，直接清除
        clearTimeout(timeoutId);

        // 重新开始计时，准备做下一个动作
        timeoutId = setTimeout(() => {
            fn.apply(_this, args);
        }, limit);
    }
}