
export const throttle = (fn, limit) => {
    let inThrottle;

    // if throttle time limit is clear
    return function () {
        const args = arguments;
        const _this = this;

        if (!inThrottle) {
            fn.apply(_this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit)
        }
    }
}