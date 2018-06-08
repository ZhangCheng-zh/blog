function throttle (fn, limit) {
    let inThrottle;

    return function (...args) {
        let _this = this;
        
        // 如果当前不在节流状态下，触发函数
        if (!inThrottle) {
            fn.apply(_this, ...args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

