export default function throttle(func, wait) {
    let lastTime = 0;

    return function throttled(...args) {
        const now = Date.now();

        // only when wait enough time, the func can be triggerred
        if (now - lastTime >= wait) {
            lastTime = now;
            func.apply(this, args);
        }
    }
}