export default function debounce (func, wait) {
    // save timer
    let timeoutID = null;

    let lastArgs;
    let lastThis;

    function cleanup() {
        // clean up
        timeoutID = null;
        lastArgs = lastThis = undefined;
    }

    function invoke() {
        func.apply(lastThis, lastArgs);
        // clean up
        cleanup();
    }

    function debounced(...args) {
        lastArgs = args;
        lastThis = this;

        // clear previous timer
        clearTimeout(timeoutID)

        timeoutID = setTimeout(invoke, wait)
    }

    debounced.cancel = function () {
        clearTimeout(timeoutID);
        cleanup()
    }

    debounced.flush = function () {
        clearTimeout(timeoutID);
        invoke(); // wll also clear timeoutID + args/this
    }

    return debounced;
}